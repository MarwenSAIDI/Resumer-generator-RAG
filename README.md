## Setup
* You must have ollama installed.
* Create a virtual environment in the project directory
* Install the requirements in the `requirements.txt` file using the command 

```
pip install -r .\requirements.txt
```

* Pull at least one LLM in Ollama to use for the embedding model and generator model (it is bes to decouple the two by installing two LLM where one is for the embedding and the other is for the generator)

## Environment variables
This project uses **Ollama** as the resource for any LLMs. in order to access it, the environment variable are in the *.env.example* file. Copy them in a *.env* file that you will create before using the API and follow the instructions.
```
GENERATOR_MODEL_NAME=<the-llm-model-name-for-the-generator>
EMBEDDING_MODEL_NAME=<the-llm-model-name-for-the-embedding>
OLLAMA_ENDPOINT=<the-ollama-endpoint>
```

## Local
First things first, you must have your *virtual environment* activated and **Ollama** is running. Once it is ready, run the command

```
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

And open the URL `http://localhost:8000/docs`

## Docker
To build the docker image:
```
docker build --no-cache -t resumer_generator:1.0 .
```

To execute the docker container:
```
docker run --env-file ./.env -p 8000:8000 resumer_generator:1.0  
```

> [!NOTICE]
>
> To use the containerized version of the API you must install the [Ollama docker image](https://hub.docker.com/r/ollama/ollama) and create a network for both containers.

## Usage
Here is a step by step guide on how to use the API.

**Step 1**
Pass your professional experiences one at a time to the route `/api/v1/retriever/embedExperience` and istall the pickle files generated.

**Step 2**
Take your job offer and pass it to the route `/api/v1/retriever/embedExperience` to extract the **job offer experiences** and the **job offer soft skills** needed in the job offer.

**Step 3**
To get the top experiences for you list of professional experiences related to the job offer details you pass to the route `/api/v1/retriever/retrieveExperiences` how many experiences you want to be returned (shouldn't be higher than the number of experiences provided), the **job offer experiences** needed in this job, and the pickled files.

**Step 4**