import json
import re
import sys
import os

import nbformat
import papermill as pm
from junit_xml import TestCase, TestSuite
from nbconvert import MarkdownExporter, HTMLExporter, RSTExporter

from notebooks import DIRECTORY


def run_notebook(input_notebook, add_nunit_attachment, parameters=None, kernel_name="ai-architecture-template"):
    """
    Used to run a notebook in the correct directory.

    Parameters
    ----------
    add_nunit_attachment :
    input_notebook : Name of Notebook to Test
    output_notebook : Name of Test Notebook Output
    parameters : Optional Parameters to pass to papermill
    :param kernel_name: Jupyter Kernal
    """

    output_notebook = input_notebook.replace(".ipynb", ".output_ipynb")
    try:
        results = pm.execute_notebook(
            os.path.join(DIRECTORY, input_notebook),
            os.path.join(DIRECTORY, output_notebook),
            parameters=parameters,
            kernel_name=kernel_name
        )

        for cell in results.cells:
            if cell.cell_type is "code":
                assert not cell.metadata.papermill.exception, "Error in Python Notebook"
    finally:
        with open(os.path.join(DIRECTORY, output_notebook)) as json_file:
            data = json.load(json_file)
            jupyter_output = nbformat.reads(json.dumps(data), as_version=nbformat.NO_CONVERT)

        markdown_exporter = MarkdownExporter()

        (body, resources) = markdown_exporter.from_notebook_node(jupyter_output)
        with open(os.path.join(DIRECTORY, output_notebook.replace(".output_ipynb", ".md")), "w") as text_file:
            sys.stderr.write(body)
            text_file.write(body)

        if add_nunit_attachment is not None:
            path = os.path.join(DIRECTORY, output_notebook.replace(".output_ipynb", ".md"))
            add_nunit_attachment(path, output_notebook)

        rst_exporter = RSTExporter()

        (body, resources) = rst_exporter.from_notebook_node(jupyter_output)
        with open(os.path.join(DIRECTORY, output_notebook.replace(".output_ipynb", ".txt")), "w") as text_file:
            sys.stderr.write(body)
            text_file.write(body)

        if add_nunit_attachment is not None:
            path = os.path.join(DIRECTORY, output_notebook.replace(".output_ipynb", ".txt"))
            add_nunit_attachment(path, output_notebook)

        regex = r'Deployed (.*) with name (.*). Took (.*) seconds.'

        with open(os.path.join(DIRECTORY, output_notebook), 'r') as file:
            data = file.read()

            test_cases = []
            for group in re.findall(regex, data):
                test_cases.append(
                    TestCase(name=group[0] + " creation", classname=input_notebook, elapsed_sec=float(group[2]),
                             status="Success"))

            ts = TestSuite("my test suite", test_cases)

            with open('test-timing-output.xml', 'w') as f:
                TestSuite.to_file(f, [ts], prettyprint=False)
