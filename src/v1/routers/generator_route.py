"""
The generator route file
"""
import os
from fastapi import APIRouter, status
from dotenv import load_dotenv
from src.v1.utils.loaders import load_config

load_dotenv('.env')
# load the config file
config = load_config(os.path.join(os.getcwd(),"config.yml"))

OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
OLLAMA_URL = os.getenv("OLLAMA_URL")
CHAIN_CONFIG = config["generater_config"]

router = APIRouter(prefix="/generator")

@router.get("/status")
def state():
    """The status of the API endpoint
    """
    return {"status": status.HTTP_200_OK}
