"""
The generator route file
"""
import os
from fastapi import APIRouter, status
from dotenv import load_dotenv
import time
import asyncio
from src.v1.utils.loaders import load_config
from src.v1.utils.loaders import RagChain
from src.v1.schemas.profile_schema import Profile
from src.v1.schemas.experience_schema import RetrievedExperience
from src.v1.schemas.resumer_schema import JobOfferDetails, Resumer
from src.v1.utils.logger import logger
from src.exceptions import *
from src.config import config

load_dotenv('.env')
# load the config file
llm_config = load_config(os.path.join(os.getcwd(),"config.yml"))

TIMEOUT = int(config['THIRD-PARTY']['timeout'])

GENERATOR_MODEL_NAME = os.getenv("GENERATOR_MODEL_NAME")
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT")
CHAIN_CONFIG = llm_config["generater_config"]

experience_filter_prompt = CHAIN_CONFIG['experience_filter_prompt']
softskills_filter_prompt = CHAIN_CONFIG['softskills_filter_prompt']
generator_prompt = CHAIN_CONFIG['generator_prompt']

# Initialize the generator
generator_obj = RagChain(
    GENERATOR_MODEL_NAME,
    OLLAMA_ENDPOINT,
    CHAIN_CONFIG['stop_tokens'],
)

logger.info("generator_route - Setting up the environment variables")

router = APIRouter(prefix="/generator", tags=["Generator"])

@router.get("/status")
def state():
    """The status of the API endpoint
    """
    return {"status": status.HTTP_200_OK}

@router.post("/jobOfferExperiences")
async def job_offer_experiences(
    jobOffer:str,
) -> JobOfferDetails:
    
    logger.info("generator_route - Passing the job offer ...")


    start = time.time()
    try:
        # get the experiences needed in the job offer
        exps = await asyncio.wait_for(generator_obj.find_experiences(jobOffer, experience_filter_prompt), timeout=TIMEOUT)

        # get the softskills needed in the job offer
        ss = await asyncio.wait_for(generator_obj.find_softskills(jobOffer, softskills_filter_prompt), timeout=TIMEOUT)

        logger.info(f"generator_route - Extracted the experiences and sofskills after {time.time() - start} seconds.")
        return JobOfferDetails(
            jobOfferExperiences=exps,
            jobOfferSofSkills=ss,
        )
    except asyncio.exceptions.TimeoutError:
        raise UnprocessedRequestError(name="Resumer generator route", message="The softskill or the expereinces generator timedout")

@router.post("/generateResumer")
async def generate_resumer(
    profile: Profile, 
    retrievedExperiences: RetrievedExperience,
    jobOfferDetails: JobOfferDetails
) -> Resumer:
    
    logger.info("generator_route - Generating the resume ...")
    start = time.time()
    try:
        # Generate Resumer
        result = await asyncio.wait_for(generator_obj.generate_resume(
            profile,
            jobOfferDetails,
            retrievedExperiences,
            generator_prompt
        ), timeout=TIMEOUT)

        logger.info(f"generator_route - Generated the resume after {time.time() - start} seconds.")
        return Resumer(
            completion=result
        )
    except asyncio.exceptions.TimeoutError:
        raise UnprocessedRequestError(name="Resumer generator route", message="The resume generator timedout")
