# arXiv Research Agent

Table of contents:

- [arXiv Research Agent](#arxiv-research-agent)
  - [Introduction](#introduction)
  - [Directory structure and file descriptions](#directory-structure-and-file-descriptions)
  - [Prerequisites](#prerequisites)
  - [Cloning and setting up the template](#cloning-and-setting-up-the-template)
  - [Running the agent locally](#running-the-agent-locally)
  - [Optional: Modify and configure the template](#optional-modify-and-configure-the-template)
  - [Testing the template](#testing-the-template)
  - [Deploying on IBM Cloud](#deploying-on-ibm-cloud)
  - [Querying the deployment](#querying-the-deployment)
    - [What's next?](#whats-next)

## Introduction

This repository provides a basic template for LLM apps built using LangGraph framework. It also makes it easy to deploy them as an AI service as part of IBM watsonx.ai for IBM Cloud[^1].

An AI service is a deployable unit of code that captures the logic of your generative AI use case. For and in-depth description of the topic please refer to the [IBM watsonx.ai documentation](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ai-services-templates.html?context=wx&audience=wdp).

[^1]: _IBM watsonx.ai for IBM Cloud_ is a full and proper name of the component we're using in this template and only a part of the whole suite of products offered in the SaaS model within IBM Cloud environment. Throughout this README, for the sake of simplicity, we'll be calling it just an **IBM Cloud**.

The template builds a ReAct agent that can browse the web for arXiv research papers and summarize these papers for you.

## Directory structure and file descriptions

The high level structure of the repository is as follows:

langgraph-arxiv-research  
 ┣ src  
 ┃ ┣ langgraph_react_agent  
 ┣ schema  
 ┣ ai_service.py  
 ┣ config.toml.example  
 ┣ pyproject.toml

- `langgraph_react_agent` folder: Contains auxiliary files used by the deployed function. They provide various framework specific definitions and extensions. This folder is packaged and sent to IBM Cloud during deployment as a [package extension](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-create-custom-software-spec.html?context=wx&audience=wdp#custom-wml).
- `schema` folder: Contains request and response schemas for the `/ai_service` endpoint queries.
- `ai_service.py` file: Contains the function to be deployed as an AI service defining the application's logic
- `config.toml` file: A configuration file with placeholders that stores the deployment metadata. After downloading the template repository, copy the contents of the `config.toml.example` file to the `config.toml` file and fill in the required fields. `config.toml` file can also be used to tweak the model for your use case. 

## Prerequisites

- [Poetry](https://python-poetry.org/) package manager,
- [Pipx](https://github.com/pypa/pipx) or [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Cloning and setting up the template

- ### Step 1: Clone the repository

  In order not to clone the whole `IBM/watsonx-developer-hub` repository we'll use git's shallow and sparse cloning feature to checkout only the template's directory:

  ```sh
  git clone --no-tags --depth 1 --single-branch --filter=tree:0 --sparse https://github.com/IBM/watsonx-developer-hub.git
  cd watsonx-developer-hub
  git sparse-checkout add agents/community/langgraph-arxiv-research/
  ```

  Move to the directory with the agent template:

  ```sh
  cd agents/community/langgraph-arxiv-research/
  ```

  > [!NOTE]
  > From now on it'll be considered that the working directory is `watsonx-developer-hub/agents/community/langgraph-arxiv-research/`

- ### Step 2: Install the template

  Running the below commands will install the repository in a separate virtual environment:

  - For `pipx`:

    ```sh
    pipx install --python 3.11 poetry # set up the env incl. poetry
    poetry install # install the dependencies
    source $(poetry -q env use 3.11 && poetry env info --path)/bin/activate # start the environment
    ```

  - For `uv`:
    ```sh
    uv venv --python 3.11 # set up the env
    uv pip install poetry # install poetry
    poetry install # install the dependencies
    ```

  You can use any other tool to run your Python code, make sure to use Python v11 or higher.

- ### Step 3: Export PYTHONPATH

  Adding working directory to `PYTHONPATH` is necessary for the next steps. In your terminal execute:

  ```sh
  export PYTHONPATH=$(pwd):${PYTHONPATH}
  ```

- ## Step 4: Set the enviroment variables

  The [config.toml](config.toml) file should be filled in before either deploying the template on IBM Cloud or executing it locally.

  Go to the [Developer Access](https://dataplatform.cloud.ibm.com/developer-access) page to find your environment variables.

Everything is now set up to run the agent locally in the next section.

## Running the agent locally

You can run the agent locally and interact with the agent via a terminal-based chat application.

- ### Step 1: Run the script for local AI service execution

  ```sh
  poetry run python examples/execute_ai_service_locally.py
  ```

- ### Step 2: Ask the agent

  Choose from some pre-defined questions or ask the agent questions of your own.

  Please bear in mind that the research paper should be available on arXiv if you want the agent to be able to summarize it.

Proceed to the next section to learn how to to modify the agent, or continue to [test](#testing-the-template) or [deploy](#deploying-on-ibm-cloud) the agent.

## Optional: Modify and configure the template

The template can also be extended to provide additional key-value data to the application. Create a special asset from within your deployment space called _Parameter Sets_. Use the _watsonx.ai_ library to instantiate it and later reference it from the code.  
For detailed description and API please refer to the [IBM watsonx.ai Parameter Set's docs](https://ibm.github.io/watsonx-ai-python-sdk/core_api.html#parameter-sets)

Sensitive data should not be passed unencrypted, e.g. in the configuration file. The recommended way to handle them is to make use of the [IBM Cloud® Secrets Manager](https://cloud.ibm.com/apidocs/secrets-manager/secrets-manager-v2). The approach to integrating the Secrets Manager's API with the app is for the user to decide on.

The [agent.py](src/langgraph_react_agent/agent.py) file builds app the graph consisting of nodes and edges. The former define the logic for agents while the latter control the logic flow in the whole graph.  
For detailed info on how to modify the graph object please refer to [LangGraph's official docs](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/#create-graph)

The [ai_service.py](ai_service.py) file encompasses the core logic of the app alongside the way of authenticating the user to the IBM Cloud.  
For a detailed breakdown of the ai-service's implementation please refer the [IBM Cloud docs](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ai-services-create.html?context=wx)

[tools.py](src/langgraph_react_agent/tools.py) file stores the definition for tools enhancing the chat model's capabilities.  
In order to add new tool create a new function, wrap it with the `@tool` decorator and add to the `TOOLS` list in the `extensions` module's [**init**.py](src/langgraph_react_agent/__init__.py)

For more sophisticated use cases (like async tools), please refer to the [langchain docs](https://python.langchain.com/docs/how_to/custom_tools/#creating-tools-from-runnables).

## Testing the template

The `tests/` directory's structure resembles the repository. Adding new tests should follow this convention.  
For exemplary purposes only the tools and some general utility functions are covered with unit tests.

Running the below command will run the complete tests suite:

```sh
poetry run pytest -r 'fEsxX' tests/
```

## Deploying on IBM Cloud

Follow these steps to deploy the model on IBM Cloud.

- ### Step 1: Fill in the `config` file

  Enter the necessary credentials in the `config.toml` file.

- ### Step 2: Run the deployment script

  ```sh
  poetry run python scripts/deploy.py
  ```

Successfully completed script will print on stdout the `deployment_id` which is necessary to locally test the deployment. For further info please refer [to the next section](#querying-the-deployment)

## Querying the deployment

Follow these steps to inference your deployment. The [query_existing_deployment.py](examples/query_existing_deployment.py) file shows how to test the existing deployment using `watsonx.ai` library.

- ### Step 1: Initialize the deployment ID

  Initialize the `deployment_id` variable in the [query_existing_deployment.py](examples/query_existing_deployment.py) file.

  The _deployment_id_ of your deployment can be obtained from [the previous section](#deploying-on-ibm-cloud) by running [scripts/deploy.sh](scripts/deploy.py)

- ### Step 2: Run the script for querying the deployment

  ```sh
  poetry run python examples/query_existing_deployment.py
  ```

### What's next?

The next step would be to integrate this agent into a web application, for example by building an API endpoint that can be accessed via your watsonx.ai deployment.
