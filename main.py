""" In this main file we test the functionalities built. """

import os
from dotenv import load_dotenv
from utils.retriever import SectionsRetriever
from utils.loaders import RagChain
from utils.loaders import load_config

load_dotenv('.env')

# load the config file
config = load_config(os.path.join(os.getcwd(),"config.yml"))

OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
OLLAMA_URL = os.getenv("OLLAMA_URL")
RETRIEVER_CONFIG = config["retriever_config"]
CHAIN_CONFIG = config["generater_config"]

# Load the retriever
retriever_obj = SectionsRetriever(OLLAMA_MODEL_NAME, OLLAMA_URL, RETRIEVER_CONFIG)

# Test retriever
EXPERIENCE_1=""""""

EXPERIENCE_2=""""""

EXPERIENCE_3=""""""

print("Process experiences ...")
json_text_1 = retriever_obj.process_experience(EXPERIENCE_1)
json_text_2 = retriever_obj.process_experience(EXPERIENCE_2)
json_text_3 = retriever_obj.process_experience(EXPERIENCE_3)


doc_1 = retriever_obj.reconstruct_experience("professional experience", json_text_1.content)
doc_2 = retriever_obj.reconstruct_experience("professional experience", json_text_2.content)
doc_3 = retriever_obj.reconstruct_experience("professional experience", json_text_3.content)

print("Add to retriever ...")
retiriever = retriever_obj.create_retriever([doc_1.content, doc_2.content, doc_3.content])

# Test the RagChain loader
chain_obj = RagChain(OLLAMA_MODEL_NAME, OLLAMA_URL, CHAIN_CONFIG)

JOB_OFFER=""""""

print("Get experiences/softskills from job offer ...")
experiences = chain_obj.find_experiences(JOB_OFFER)

softskills = chain_obj.find_softskills(JOB_OFFER)

# Generate resumer
details = {}

print("Generate resumer ...")
resumer = chain_obj.generate_resume(details, softskills.content, experiences.content, retiriever)

print("*"*20)
print(resumer.content)
