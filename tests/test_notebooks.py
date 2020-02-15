"""
ai-architecture-template - test_notebooks.py

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
import pytest

from tests.utils import run_notebook

@pytest.mark.parametrize(
    "notebook",
    ['00_AMLConfiguration.ipynb'],
)
def test_notebook(notebook, add_nunit_attachment):
    run_notebook(notebook, add_nunit_attachment)
