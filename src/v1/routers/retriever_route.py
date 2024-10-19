"""
The retriever route file
"""
import os
from fastapi import APIRouter, status, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from uuid import uuid1
import pickle
import time
import asyncio
from starlette.background import BackgroundTasks
from src.v1.utils.retriever import SectionsRetriever
from src.v1.utils.loaders import load_config
from src.v1.utils.logger import logger
from src.v1.schemas.experience_schema import RetrievedExperience
from src.exceptions import *
from src.config import config

load_dotenv('.env')
# load the config file
llm_config = load_config(os.path.join(os.getcwd(),"config.yml"))

TIMEOUT = int(config['THIRD-PARTY']['timeout'])

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT")
RETRIEVER_CONFIG = llm_config["retriever_config"]

retriever_obj = SectionsRetriever(EMBEDDING_MODEL_NAME, OLLAMA_ENDPOINT)

if not os.path.exists(os.path.join(os.getcwd(), 'data')):
    os.mkdir(os.path.join(os.getcwd(), 'data'))

logger.info("retriever_route - Setting up the environment variables")

def del_files(job='delete files'):
    """A background task that deletes unnecessary files.

    Args:
        job (str, optional): The job title. Defaults to 'delete files'.

    Raises:
        ValueError: If a problem occures
    """
    
    pkl_files = os.listdir("data")
    try:
        if pkl_files != []:
            for p in pkl_files:
                os.unlink(os.path.join(os.getcwd(), "data", p))
        else:
            raise ValueError("There are no files to delete")
        logger.info(f"retriever_route ({job}) - All files have been deleted")
    except Exception as e:
        logger.warning(f"retriever_route ({job}) - {e.args[0]}")


router = APIRouter(prefix="/retriever", tags=["Retriever"])

@router.get("")
def state():
    """The status of the API endpoint
    """
    return {"status": status.HTTP_200_OK}



@router.post("/embedExperience")
async def embed_experience(experience:str, background_tasks: BackgroundTasks):
    """This endpoint creates an embedding of the experience provided and returns a
    pickle file with embeddings.

    Args:
        experience (str): The unstructured experience text

    Returns:
        Pickle file: a pickeled file of the embedding
    """
    logger.info("retriever_route - Passing the experience to the embedding model")


    start = time.time()
    try:
        obj_experience = await asyncio.wait_for(retriever_obj.create_embedding(experience), timeout=TIMEOUT)
        file_name = f"experience_{uuid1()}.pkl"
        with open(f"data/{file_name}", "wb") as f:
            pickle.dump(obj_experience, f)

        logger.info(f"retriever_route - Compressed the zip object after {time.time() - start} seconds.")
        background_tasks.add_task(del_files)
        return FileResponse(f"data/{file_name}", media_type='application/octet-stream', filename=file_name)
    
    except asyncio.exceptions.TimeoutError:
        raise UnprocessedRequestError(name="Resumer retiever route", message="The embedding model Timed out")

@router.post("/retrieveExperiences")
async def retrieve_experiences(
    jobOfferExperiences:str,
    maxExperiences:int,
    filesContents: list[UploadFile]
) -> RetrievedExperience:
    
    # load the experiences into the retriever
    files = []
    for f in filesContents:
            f = pickle.load(f.file)
            files.append(f)
    
    retriever_obj.set_retriever(files, maxExperiences)

    # get the relevant experiences
    try:
        exps = await asyncio.wait_for(retriever_obj.get_relevant_experiences(jobOfferExperiences), timeout=TIMEOUT)
        logger.info("retriever_route - Sucessfully retrieved the contexts")

        return RetrievedExperience(
            contents=exps,
        )
    except asyncio.exceptions.TimeoutError:
        raise UnprocessedRequestError(name="Resumer retiever route", message="The retriever Timed out")
    