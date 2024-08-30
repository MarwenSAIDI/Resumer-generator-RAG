""" In this main file we test the functionalities built. """

import os
from dotenv import load_dotenv
from utils.retriever import SectionsRetriever
from utils.loaders import load_config

load_dotenv('.env')

# load the config file
config = load_config(os.path.join(os.getcwd(),"config.yml"))

OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
OLLAMA_URL = os.getenv("OLLAMA_URL")
RETRIEVER_CONFIG = config["retriever_config"]

# Load the retriever
retriever_obj = SectionsRetriever(OLLAMA_MODEL_NAME, OLLAMA_URL, RETRIEVER_CONFIG)

# Test retriever
EXPERIENCE=""""""
json_text = retriever_obj.process_experience(EXPERIENCE)

print(json_text.content)

print("---------------------")

doc = retriever_obj.reconstruct_experience("professional experience", json_text)

print(doc.content)
print("---------------------")


print(retriever_obj.create_retriever([doc.content]))
