"""
The retriever route file
"""
import os
import json
from fastapi import APIRouter, status
from dotenv import load_dotenv
from src.v1.utils.retriever import SectionsRetriever
from src.v1.utils.loaders import load_config
from src.v1.schemas.experience_schema import Experience, ExperienceContent

load_dotenv('.env')
# load the config file
config = load_config(os.path.join(os.getcwd(),"config.yml"))

OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
OLLAMA_URL = os.getenv("OLLAMA_URL")
RETRIEVER_CONFIG = config["retriever_config"]

retriever_obj = SectionsRetriever(OLLAMA_MODEL_NAME, OLLAMA_URL, RETRIEVER_CONFIG['stop_tokens'])
experience_content_schema = RETRIEVER_CONFIG['experience_content_schema']
experience_schema = RETRIEVER_CONFIG['experience_schema']
extraction_prompt = RETRIEVER_CONFIG['experience_extraction_prompt']


router = APIRouter(prefix="/retriever")

@router.get("")
def state():
    """The status of the API endpoint
    """
    return {"status": status.HTTP_200_OK}

@router.post("/structureExperience", response_model=Experience)
def structure_experience(experience:str) -> Experience:
    """This endpoint structures the text of the experience provided by
    into a JSON format.

    Args:
        experience (str): The unstructured experience text

    Returns:
        Experience: A structured experience format
    """
    obj_content = retriever_obj.process_experience(
        experience,
        experience_content_schema,
        extraction_prompt
    )
    obj_exp = retriever_obj.process_experience(
        experience,
        experience_schema,
        extraction_prompt
    )

    data_exp_content = json.loads(obj_content.content)
    data_exp = json.loads(obj_exp.content)

    content = ExperienceContent(
        skills=data_exp_content['skills'],
        accomplishments=data_exp_content['accomplishments']
    )
    exp = Experience(
        experienceId=0,
        roleName=data_exp['roleName'],
        companyName=data_exp['companyName'],
        datePeriod=data_exp['datePeriod'],
        location=data_exp['location'],
        experienceContent=content
    )
    return exp.model_dump()

@router.post("/rewriteExperience", response_model=dict)
def rewrite_experience(experience:Experience) -> dict:
    print(experience)
    return {'rewrite': ""}