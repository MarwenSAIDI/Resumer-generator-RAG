from utils.retriever import SectionsRetriever
import os
from dotenv import load_dotenv

load_dotenv('.env')

# Load the retriever
retriever_obj = SectionsRetriever(
    os.getenv("OLLAMA_MODEL_NAME"), 
    os.getenv("OLLAMA_URL"),
    os.path.join(os.getcwd(),"config.yml")
)

# Test retriever
# print(retriever_obj.embedder.embed_query("This is query test"))