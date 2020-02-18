"""
ai-architecture-template - test_notebooks.py

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

import glob

import pytest

from notebooks import DIRECTORY


@pytest.mark.parametrize(
    "notebook",
    glob.glob(DIRECTORY + "/*.ipynb")
)
def test_notebook(notebook, add_nunit_attachment):
    from azure_utils.dev_ops.testing_utilities import run_notebook
    run_notebook(notebook, add_nunit_attachment, kernel_name="az-ml-realtime-score", root=DIRECTORY)
