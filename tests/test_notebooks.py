"""
ai-architecture-template - test_notebooks.py

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
import os
import re
import sys

import papermill as pm
from azure_utils.machine_learning.utils import load_configuration
from junit_xml import TestSuite, TestCase


def test_00_aml_configuration(add_nunit_attachment):
    cfg = load_configuration("../workspace_conf.yml")

    subscription_id = cfg['subscription_id']
    resource_group = cfg['resource_group']
    workspace_name = cfg['workspace_name']
    workspace_region = cfg['workspace_region']

    parameters = dict(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name,
                      workspace_region=workspace_region)

    run_notebook('00_AMLConfiguration.ipynb', '00_AMLConfiguration.output_ipynb', parameters, add_nunit_attachment)


def test_01_aml_configuration(add_nunit_attachment):
    run_notebook('01_DataPrep.ipynb', '01_DataPrep.output_ipynb', add_nunit_attachment=add_nunit_attachment)


def test_02_aml_configuration(add_nunit_attachment):
    run_notebook('02_TrainOnLocal.ipynb', '02_TrainOnLocal.output_ipynb', add_nunit_attachment=add_nunit_attachment)


def test_03_aml_configuration(add_nunit_attachment):
    run_notebook('03_DevelopScoringScript.ipynb', '03_DevelopScoringScript.output_ipynb',
                 add_nunit_attachment=add_nunit_attachment)


def test_04_aml_configuration(add_nunit_attachment):
    run_notebook('04_CreateImage.ipynb', '04_CreateImage.output_ipynb', add_nunit_attachment=add_nunit_attachment)


def test_05_aml_configuration(add_nunit_attachment):
    run_notebook('05_DeployOnAKS.ipynb', '05_DeployOnAKS.output_ipynb', add_nunit_attachment=add_nunit_attachment)


def test_06_aml_configuration(add_nunit_attachment):
    run_notebook('06_SpeedTestWebApp.ipynb', '06_SpeedTestWebApp.output_ipynb',
                 add_nunit_attachment=add_nunit_attachment)


def test_07_aml_configuration(add_nunit_attachment):
    run_notebook('07_RealTimeScoring.ipynb', '07_RealTimeScoring.output_ipynb',
                 add_nunit_attachment=add_nunit_attachment)


def run_notebook(input_notebook, output_notebook, parameters=None, add_nunit_attachment=None):
    """
    Used to run a notebook in the correct directory.

    Parameters
    ----------
    add_nunit_attachment :
    input_notebook : Name of Notebook to Test
    output_notebook : Name of Test Notebook Output
    parameters : Optional Parameters to pass to papermill
    """

    try:
        results = pm.execute_notebook(
            "notebooks/" + input_notebook,
            "notebooks/" + output_notebook,
            parameters=parameters,
            kernel_name="az-ml-realtime-score"
        )

        for cell in results.cells:
            if cell.cell_type is "code":
                assert not cell.metadata.papermill.exception, "Error in Python Notebook"
    finally:
        import nbformat
        jupyter_output = nbformat.reads("notebooks/" + output_notebook, as_version=nbformat.NO_CONVERT)

        from nbconvert import MarkdownExporter
        markdown_exporter = MarkdownExporter()
        markdown_exporter.template_file = 'basic'
        (body, resources) = markdown_exporter.from_notebook_node(jupyter_output)
        with open(output_notebook.replace(".output_ipynb", ".md"), "w") as text_file:
            sys.stderr.write(body)
            text_file.write(body)

        if add_nunit_attachment is not None:
            path = os.path.join(os.path.abspath('notebooks/'), output_notebook.replace(".output_ipynb", ".md"))
            add_nunit_attachment(path, output_notebook)

        regex = r'Deployed (.*) with name (.*). Took (.*) seconds.'

        with open('notebooks/' + output_notebook, 'r') as file:
            data = file.read()

            test_cases = []
            for group in re.findall(regex, data):
                test_cases.append(
                    TestCase(name=group[0] + " creation", classname='00_AMLConfiguration', elapsed_sec=float(group[2]),
                             status="Success"))

            ts = TestSuite("my test suite", test_cases)

            with open('test-timing-output.xml', 'w') as f:
                TestSuite.to_file(f, [ts], prettyprint=False)
