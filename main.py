from utils.retriever import SectionsRetriever
from utils.loaders import load_config
import os
from dotenv import load_dotenv

load_dotenv('.env')


print(os.getenv("OLLAMA_URL"))

# load the config file
config = load_config(os.path.join(os.getcwd(),"config.yml"))

# Load the retriever
retriever_obj = SectionsRetriever(
    os.getenv("OLLAMA_MODEL_NAME"), 
    os.getenv("OLLAMA_URL"),
    config["retriever_config"]
)

# Test retriever
experience="""I worked at the company Lambda ste as an AI engineer starting from January 2020 till now.
In my experience I worked on building smart assistance that iproved productivity in our solution by 60%. 
And I lead a team of 3 engineers and ditributed the work given between them.
"""
json_text = retriever_obj.process_experience(experience)

print(json_text.content)

print("---------------------")

doc = retriever_obj.reconstruct_experience("professional experience", json_text)

print(doc.content)
print("---------------------")


print(retriever_obj.create_retriever([doc.content]))