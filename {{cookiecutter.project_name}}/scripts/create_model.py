# Copyright (C) Microsoft Corporation.  All rights reserved.
import logging.config
import os
import argparse
import pandas as pd
import lightgbm as lgb
from sklearn.feature_extraction import text
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.externals import joblib
from ItemSelector import ItemSelector
from label_rank import label_rank
from azureml.core import Run


def main(args):

    run = Run.get_context()

    # The training and testing datasets.
    inputs_path = args.inputs
    data_path = os.path.join(inputs_path, args.train_data)
    test_path = os.path.join(inputs_path, args.test_data)

    # Create the outputs folder.
    outputs_path = args.outputs
    os.makedirs(outputs_path, exist_ok=True)
    model_path = os.path.join(outputs_path, args.model)
    instances_path = os.path.join(outputs_path, args.instances)
    labels_path = os.path.join(outputs_path, args.labels)

    train = _load_trainining_data(data_path)

    # Limit the number of duplicate-original question matches.
    train = train[train.n < args.match]

    # Define the roles of the columns in the training data.
    feature_columns = ["Text_x", "Text_y"]
    label_column = "Label"
    duplicates_id_column = "Id_x"
    answer_id_column = "AnswerId_y"

    # Report on the training dataset: the number of rows and the proportion of true matches.
    logger.info(
        "train: {:,} rows with {:.2%} matches".format(
            train.shape[0], train[label_column].mean()
        )
    )

    weight_column = _compute_weights(args, label_column, train)

    # Collect the unique ids that identify each original question's answer.
    labels = sorted(train[answer_id_column].unique())
    label_order = pd.DataFrame({"label": labels})

    # Collect the parts of the training data by role.
    train_X = train[feature_columns]
    train_y = train[label_column]
    sample_weight = train[weight_column]

    # Use the inputs to define the hyperparameters used in training.
    n_estimators = args.estimators
    min_child_samples = args.min_child_samples
    if args.ngrams > 0:
        ngram_range = (1, args.ngrams)
    else:
        ngram_range = None

    model = _create_model_pipeline(
        args, feature_columns, min_child_samples, n_estimators, ngram_range
    )

    train_model(args, model, model_path, sample_weight, train_X, train_y)

    test = test_model(feature_columns, label_column, model, test_path)

    test_score = _compute_scores(answer_id_column, duplicates_id_column, test)

    _report_test_results(args, run, test_score)

    # Write the scored instances to a file, along with the ordered original questions's answer ids.
    test_score.to_csv(instances_path, sep="\t", index=False, encoding="latin1")
    label_order.to_csv(labels_path, sep="\t", index=False)


def _report_test_results(args, run, test_score):
    # Compute the fraction of correct original questions by minimum rank. Also print the average rank of the correct original questions.
    for i in range(1, args.rank + 1):
        logger.info(
            "Accuracy @{} = {:.2%}".format(i, (test_score["Ranks"] <= i).mean())
        )
        run.log("Accuracy @{}".format(i), (test_score["Ranks"] <= i).mean())
    mean_rank = test_score["Ranks"].mean()
    logger.info("Mean Rank {:.4f}".format(mean_rank))
    run.log("Mean Rank", mean_rank)


def _compute_scores(answer_id_column, duplicates_id_column, test):
    # Collect the probabilities for each duplicate question, ordered by the original question ids.
    # Order the testing data by duplicate question id and original question id.
    test.sort_values([duplicates_id_column, answer_id_column], inplace=True)
    # Extract the ordered probabilities.
    probabilities = test.probabilities.groupby(
        test[duplicates_id_column], sort=False
    ).apply(lambda x: tuple(x.values))
    # Create a data frame with one row per duplicate question, and make it contain the model's predictions for each duplicate.
    test_score = (
        test[["Id_x", "AnswerId_x", "Text_x"]]
        .drop_duplicates()
        .set_index(duplicates_id_column)
    )
    test_score["probabilities"] = probabilities
    test_score.reset_index(inplace=True)
    test_score.columns = ["Id", "AnswerId", "Text", "probabilities"]
    # Evaluate the predictions
    # For each duplicate question, find the rank of its correct original question.
    test_score["Ranks"] = test_score.apply(
        lambda x: label_rank(x.AnswerId, x.probabilities, label_order.label), axis=1
    )
    return test_score


def test_model(feature_columns, label_column, model, test_path):
    # Test the model
    # Read in the test data set, and report of the number of its rows and proportion of true matches.
    logger.info("Reading {}".format(test_path))
    test = pd.read_csv(test_path, sep="\t", encoding="latin1")
    logger.info(
        "test: {:,} rows with {:.2%} matches".format(
            test.shape[0], test[label_column].mean()
        )
    )
    # Collect the model predictions. This step should take about 1 minute on a Standard NC6 DLVM.
    logger.info("Testing...")
    test_X = test[feature_columns]
    test["probabilities"] = model.predict_proba(test_X)[:, 1]
    return test


def train_model(args, model, model_path, sample_weight, train_X, train_y):
    # Fit the model.
    logger.info("Training...")
    model.fit(train_X, train_y, model__sample_weight=sample_weight)
    # Save the model to a file, and report on its size.
    if args.save:
        joblib.dump(model, model_path)
        logger.info(
            "{} size: {:.2f} MB".format(
                model_path, os.path.getsize(model_path) / (2 ** 20)
            )
        )


def _create_model_pipeline(
    args, feature_columns, min_child_samples, n_estimators, ngram_range
):
    # Verify that the hyperparameter values are valid.
    assert n_estimators > 0
    assert min_child_samples > 1
    assert type(ngram_range) is tuple and len(ngram_range) == 2
    assert ngram_range[0] > 0 and ngram_range[0] <= ngram_range[1]
    # Define the pipeline that featurizes the text columns.
    featurization = [
        (
            column,
            make_pipeline(
                ItemSelector(column), text.TfidfVectorizer(ngram_range=ngram_range)
            ),
        )
        for column in feature_columns
    ]
    features = FeatureUnion(featurization)
    # Define the estimator that learns how to classify duplicate-original question pairs.
    estimator = lgb.LGBMClassifier(
        n_estimators=n_estimators,
        min_child_samples=min_child_samples,
        verbose=args.verbose,
    )
    # Define the model pipeline as feeding the features into the estimator.
    model = Pipeline([("features", features), ("model", estimator)])
    return model


def _compute_weights(args, label_column, train):
    # Compute the instance weights used to correct for class imbalance in training.
    weight_column = "Weight"
    if args.unweighted:
        weight = pd.Series([1.0], train[label_column].unique())
    else:
        label_counts = train[label_column].value_counts()
        weight = train.shape[0] / (label_counts.shape[0] * label_counts)
    train[weight_column] = train[label_column].apply(lambda x: weight[x])
    return weight_column


def _load_trainining_data(data_path):
    # Load the training data
    print("Reading {}".format(data_path))
    train = pd.read_csv(data_path, sep="\t", encoding="latin1")
    return train


if __name__ == "__main__":
    logging.config.fileConfig(os.getenv("LOG_CONFIG", "logging.ini"))

    # Define the arguments.
    parser = argparse.ArgumentParser(
        description="Fit and evaluate a model based on train-test datasets."
    )
    parser.add_argument(
        "-d",
        "--train_data",
        help="the training dataset name",
        default="balanced_pairs_train.tsv",
    )
    parser.add_argument(
        "-t",
        "--test_data",
        help="the test dataset name",
        default="balanced_pairs_test.tsv",
    )
    parser.add_argument(
        "-i",
        "--estimators",
        help="the number of learner estimators",
        type=int,
        default=8000,
    )
    parser.add_argument(
        "--min_child_samples",
        help="the minimum number of samples in a child(leaf)",
        type=int,
        default=20,
    )
    parser.add_argument(
        "-v", "--verbose", help="the verbosity of the estimator", type=int, default=-1
    )
    parser.add_argument(
        "-n", "--ngrams", help="the maximum size of word ngrams", type=int, default=1
    )
    parser.add_argument(
        "-u",
        "--unweighted",
        help="do not use instance weights",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-m",
        "--match",
        help="the maximum number of duplicate matches",
        type=int,
        default=20,
    )
    parser.add_argument("--outputs", help="the outputs directory", default=".")
    parser.add_argument("--inputs", help="the inputs directory", default=".")
    parser.add_argument(
        "-s", "--save", help="save the model", action="store_true", default=True
    )
    parser.add_argument("--model", help="the model file", default="model.pkl")
    parser.add_argument("--instances", help="the instances file", default="inst.txt")
    parser.add_argument("--labels", help="the labels file", default="labels.txt")
    parser.add_argument(
        "-r", "--rank", help="the maximum rank of correct answers", type=int, default=3
    )
    args = parser.parse_args()

    main(args)
