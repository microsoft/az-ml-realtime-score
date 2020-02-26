[![Build Status](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_apis/build/status/AGCE%20AI/Happy%20Path%20Builds/ai-architecture-template?branchName=master)](https://dev.azure.com/AZGlobal/Azure%20Global%20CAT%20Engineering/_build/latest?definitionId=170&branchName=master)
TODO: Insert Build Badge Here
### Authors: <>
### Acknowledgements: <>

# AI Architecture Template

## Overview
TODO: Insert Overview Here

## Design
TODO: Insert Design Here

## Prerequisites
1. [Anaconda Python](https://www.anaconda.com/download)
1. [Docker](https://docs.docker.com/v17.12/install/linux/docker-ee/ubuntu) installed.
1. [Azure account](https://azure.microsoft.com).

---
**NOTE**
You will need to be able to run docker commands without sudo to run this tutorial. Use the following commands to do
this.

```bash
sudo usermod -aG docker $USER
newgrp docker
``` 
---

The tutorial was developed on an [Azure Ubuntu
DSVM](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro),
which addresses the first three prerequisites.

## Setup

To set up your environment to run these notebooks, please follow these steps.  They setup the notebooks to use Azure
seamlessly.

1. Fork this repo into your own Github Namespace or import this repo into Azure DevOps.
1. Copy `project_sample.yml` to a new file, `project.yml`, and fill in each field. This will keep secrets out of the 
source code, and this file will be ignored by git.
1. Clone your repository locally, or on an Azure Data Science Virtual Machine.
   ```
   git clone https://github.com/[your_github_username]/ai-architecture-template.git
   ```
1. Enter the local repository:
   ```
   cd ai-architecture-template
   ```
1. Create the Python ai-architecture-template virtual environment using the environment.yml:
   ```
   conda env create -f environment.yml
   ```
1. Activate the virtual environment:
   ```
   source activate ai-architecture-template
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
1. If you have more than one Azure subscription, select it:
   ```
   az account set --subscription <Your Azure Subscription>
   ```
1. Start the Jupyter notebook server:
	```
	jupyter notebook
	
You may also use the .ci/azure-pipeline.yml to configure a CI/CD build for your repostitory. Follow the directions
provided within the pipeline.

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

[Microsoft AI Github](https://github.com/microsoft/ai) Find other Best Practice projects, and Azure AI Designed patterns
 in our central repository. 
