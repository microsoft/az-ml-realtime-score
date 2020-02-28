"""
ai-architecture-template - test_notebooks.py

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
import pytest

from azure_utils.dev_ops.testing_utilities import run_notebook

from notebooks import directory


@pytest.mark.parametrize(
    "notebook",
    [
        directory + "/00_AMLConfiguration.ipynb",
        directory + "/01_DataPrep.ipynb",
        directory + "/02_TrainOnLocal.ipynb",
        directory + "/03_DevelopScoringScript.ipynb",
        directory + "/04_CreateImage.ipynb",
        directory + "/05_DeployOnAKS.ipynb"
    ]
)
def test_notebook(notebook, add_nunit_attachment):
    """ Test Notebooks and Save Output to Text Files"""
    run_notebook(notebook, add_nunit_attachment, kernel_name="az-ml-realtime-score", root=directory)
