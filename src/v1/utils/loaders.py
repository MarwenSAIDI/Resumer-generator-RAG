""" Build the loaders for the main LLM and the config file """

import yaml
from typing import List
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from src.v1.schemas.profile_schema import Profile
from src.v1.schemas.experience_schema import RetrievedExperience
from src.v1.schemas.resumer_schema import JobOfferDetails
from src.v1.utils.logger import logger

def load_config(config_file:str):
    """_summary_

    Args:
        config_file (str): _description_

    Returns:
        _type_: _description_
    """
    # Load configs
    with open(config_file, 'r', encoding='utf-8') as stream:
        config = yaml.safe_load(stream)
    return config

class RagChain:
    """_summary_
    """

    def __init__(self, model_name:str, url:str, stop_tokens: List[str]) -> None:
        """_summary_

        Args:
            model_name (str): _description_
            url (str): _description_
            config (_type_): _description_
            retriever (_type_, optional): _description_. Defaults to None.
        """

        # Load the chat LLM
        self.llm = ChatOllama(
            model=model_name,
            base_url=url,
            stop=stop_tokens
        )

    async def find_experiences(self, job_offer: str, experience_filter_prompt: str):
        """_summary_
        """
        prompt = PromptTemplate.from_template(experience_filter_prompt)

        res = await self.llm.ainvoke(prompt.format(job_offer=job_offer))
        logger.info("generator - Extracted the experiences")

        return res.content
    async def find_softskills(self, job_offer: str, softskills_filter_prompt: str):
        """_summary_
        """
        prompt = PromptTemplate.from_template(softskills_filter_prompt)

        res = await self.llm.ainvoke(prompt.format(job_offer=job_offer))
        logger.info("generator - Extracted the softskills")

        return res.content
    async def generate_resume(
            self,
            candidate_profile: Profile,
            job_offer_details: JobOfferDetails,
            candidate_experiences: RetrievedExperience,
            generator_prompt: str,
        ):
        """_summary_

        Args:
            result_softskills (_type_): _description_
            retriever (_type_): _description_
        """
        context = "\n".join(text for text in candidate_experiences.contents)
        prompt = PromptTemplate.from_template(generator_prompt)
        query = prompt.format(
            profile=candidate_profile.model_dump(),
            experiences_company=job_offer_details.model_dump(),
            experience_context=context)
        
        res = await self.llm.ainvoke(query)

        logger.info("generator - Sucessfully genrated the resume")
        return res.content

