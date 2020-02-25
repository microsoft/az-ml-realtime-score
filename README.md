[![Build Status](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_apis/build/status/AGCE%20AI/Happy%20Path%20Builds/AI%20ML%20RTS?branchName=master)](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_build/latest?definitionId=118&branchName=master)
### Authors: Fidan Boylu Uz, Yan Zhang
### Acknowledgements: Mario Bourgoin, Mathew Salvaris

# Deploying Python models for real-time scoring using Azure Machine Learning

In this repository there are a number of tutorials in Jupyter notebooks that have step-by-step instructions on (1) how to train a machine learning model using Python; (2) how to deploy a trained machine learning model throught Azure Machine Learning (AzureML). The tutorials cover how to deploy models on following deployment target:

## Overview
This scenario shows how to deploy a Frequently Asked Questions (FAQ) matching model as a web service to provide predictions for user questions. For this scenario, “Input Data” in the [architecture diagram](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/realtime-scoring-python) refers to text strings containing the user questions to match with a list of FAQs. The scenario is designed for the Scikit-Learn machine learning library for Python but can be generalized to any scenario that uses Python models to make real-time predictions.

## Design
<!-- ![alt text](Design.png "Design") -->
The scenario uses a subset of Stack Overflow question data which includes original questions tagged as JavaScript, their duplicate questions, and their answers. It trains a Scikit-Learn pipeline to predict the match probability of a duplicate question with each of the original questions. These predictions are made in real time using a REST API endpoint.
The application flow for this architecture is as follows:
1.	The client sends a HTTP POST request with the encoded question data.
2.	The  webservice extracts the question from the request
3.	The question is then sent to the Scikit-learn pipeline model for featurization and scoring. 
4.	The matching FAQ questions with their scores are then piped into a JSON object and returned to the client.

An example app that consumes the results is included with the scenario.

## Prerequisites
1. Linux (Ubuntu).
1. [Anaconda Python](https://www.anaconda.com/download)
1. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
1. [Azure account](https://azure.microsoft.com).


---
**NOTE**
You will need to be able to run docker commands without sudo to run this tutorial. Use the following commands to do this.

```bash
sudo usermod -aG docker $USER
newgrp docker
``` 
---

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

## Setup

To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Azure seamlessly.

1. Create a _Linux_ _Ubuntu_ VM.
1. Log in to your VM.  We recommend that you use a graphical client
   such as
   [X2Go](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro#x2go)
   to access your VM.  The remaining steps are to be done on the VM.
1. Open a terminal emulator.
1. Clone, fork, or download the zip file for this repository:
   ```
   git clone https://github.com/Microsoft/az-ml-realtime-score.git
   ```
1. Enter the local repository:
   ```
   cd az-ml-realtime-score
   ```
1. Copy `sample_workspace_conf.yml` to a new file, `workspace_conf.yml`, and fill in each field. This will keep secrets out of the source code, and this file will be ignored by git.
1. Create the Python az-ml-realtime-score virtual environment using the environment.yml:
   ```
   conda env create -f environment.yml
   ```
1. Activate the virtual environment:
   ```
   source activate az-ml-realtime-score
   ```
   The remaining steps should be done in this virtual environment.
1. Login to Azure:
   ```
   az login
   ```
   You can verify that you are logged in to your subscription by executing
   the command:
   ```
   az account show -o table
   ```
1. Start the Jupyter notebook server:
   ```
   jupyter notebook
   ```

# Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.


# Related projects

[Microsoft AI Github](https://github.com/microsoft/ai) Find other Best Practice projects, and Azure AI Designed patterns in our central repository. 
