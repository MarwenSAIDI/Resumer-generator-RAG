"""
The retriever route file
"""
from fastapi import APIRouter, status
import os
from src.v1.utils.retriever import SectionsRetriever
from src.v1.utils.loaders import load_config
from dotenv import load_dotenv

load_dotenv('.env')
# load the config file
config = load_config(os.path.join(os.getcwd(),"config.yml"))

OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
OLLAMA_URL = os.getenv("OLLAMA_URL")
RETRIEVER_CONFIG = config["retriever_config"]

router = APIRouter(prefix="retriever")

@router.get("/status")
def status():
    return {"status": status.HTTP_200_OK}