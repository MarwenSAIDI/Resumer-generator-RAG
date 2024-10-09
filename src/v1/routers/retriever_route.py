"""
The retriever route file
"""
import os
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

retriever_obj = SectionsRetriever(OLLAMA_MODEL_NAME, OLLAMA_URL, RETRIEVER_CONFIG)


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
    # data = retriever_obj.process_experience(experience)
    # data = json.loads(data)
    print(experience)
    print(Experience.model_json_schema())

    # Example
    content = ExperienceContent(
        companyName="string",
        startDate="Jun 2022",
        endDate="July 2022",
        location="Tunis",
        skills=["a", "b", "c"],
        accomplishments=["a", "b", "c"]
    )
    exp = Experience(
        experienceId=0,
        roleName="s",
        experienceContent=content
    )

    # content = ExperienceContent(
    #     companyName=data['companyName'],
    #     startDate=data['startDate'],
    #     endDate=data['endDate'],
    #     location=data['location'],
    #     skills=data['skills'],
    #     accomplishments=data['accomplishments']
    # )
    # exp = Experience(
    #     experienceId=0,
    #     roleName=data['roleName'],
    #     experienceContent=content
    # )
    return exp.model_dump()
