## Setup
* You must have ollama installed.
* Create a virtual environment in the project directory
* Install the requirements in the `requirements.txt` file using the command 

```
pip install -r .\requirements.txt
```
## Environment variables
This project uses **Ollama** as the resource for any LLMs. in order to access it, the environment variable are in the *.env.example* file. Copy them in a *.env* file that you will create before using the API and follow the instructions.
```
GENERATOR_MODEL_NAME=<the-llm-model-name-for-the-generator>
EMBEDDING_MODEL_NAME=<the-llm-model-name-for-the-embedding>
OLLAMA_ENDPOINT=<the-ollama-endpoint>
```

## Docker
To build the docker image:
```
docker build --no-cache -t resumer_generator:1.0 .
```

To execute the docker container:
```
docker run --env-file ./.env -p 8000:8000 resumer_generator:1.0  
```

## Usage
Here is a step by step guide on how to use the API.

**Step 1**

**Step 2**