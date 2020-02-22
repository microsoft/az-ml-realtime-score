"""
ai-architecture-template - test_notebooks.py

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

import glob

import pytest

from azure_utils.dev_ops.testing_utilities import run_notebook
from notebooks import DIRECTORY


@pytest.mark.parametrize(
    "notebook",
    [
        DIRECTORY + "/00_AMLConfiguration.ipynb",
        DIRECTORY + "/01_DataPrep.ipynb",
        DIRECTORY + "/02_TrainOnLocal.ipynb",
        DIRECTORY + "/03_DevelopScoringScript.ipynb",
        DIRECTORY + "/04_CreateImage.ipynb",
        DIRECTORY + "/05_DeployOnAKS.ipynb"
    ]
)
def test_notebook(notebook, add_nunit_attachment):
    run_notebook(notebook, add_nunit_attachment, kernel_name="az-ml-realtime-score", root=DIRECTORY)
