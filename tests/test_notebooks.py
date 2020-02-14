"""
ai-architecture-template - test_notebooks.py

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
import re
import os

import papermill as pm
from azure_utils.machine_learning.utils import load_configuration
from junit_xml import TestSuite, TestCase


def test_00_aml_configuration():
    cfg = load_configuration("../workspace_conf.yml")

    subscription_id = cfg['subscription_id']
    resource_group = cfg['resource_group']
    workspace_name = cfg['workspace_name']
    workspace_region = cfg['workspace_region']

    parameters = dict(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name,
                      workspace_region=workspace_region)

    run_notebook('00_AMLConfiguration.ipynb', '00_AMLConfiguration.output_ipynb', parameters)

    path = os.path.dirname(os.path.abspath(__file__))
    if "test" in os.path.dirname(os.path.abspath(__file__)):
        os.chdir("../notebooks")
    elif "notebooks" not in os.path.dirname(os.path.abspath(__file__)):
        os.chdir("notebooks")

    regex = r'Deployed (.*) with name (.*). Took (.*) seconds.'

    with open('00_AMLConfiguration.output_ipynb', 'r') as file:
        data = file.read()

        test_cases = []
        for group in re.findall(regex, data):
            test_cases.append(
                TestCase(name=group[0] + " creation", classname='00_AMLConfiguration', elapsed_sec=float(group[2]),
                         status="Success"))

        ts = TestSuite("my test suite", test_cases)

        with open('test-timing-output.xml', 'w') as f:
            TestSuite.to_file(f, [ts], prettyprint=False)

    os.chdir(path)

def test_01_aml_configuration():
    run_notebook('01_DataPrep.ipynb', '01_DataPrep.output_ipynb')


def test_02_aml_configuration():
    run_notebook('02_TrainOnLocal.ipynb', '02_TrainOnLocal.output_ipynb')


def run_notebook(input_notebook, output_notebook, parameters=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if "test" in os.path.dirname(os.path.abspath(__file__)):
        os.chdir("../notebooks")
    elif "notebooks" not in os.path.dirname(os.path.abspath(__file__)):
        os.chdir("notebooks")

    results = pm.execute_notebook(
        input_notebook,
        output_notebook,
        parameters=parameters,
        kernel_name="az-ml-realtime-score"
    )

    for cell in results.cells:
        if cell.cell_type is "code":
            assert not cell.metadata.papermill.exception, "Error in Python Notebook"

    os.chdir(path)
