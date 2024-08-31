""" Build the loaders for the main LLM and the config file """

from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
import yaml

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

    def __init__(self, model_name:str, url:str, config) -> None:
        """_summary_

        Args:
            model_name (str): _description_
            url (str): _description_
            config (_type_): _description_
            retriever (_type_, optional): _description_. Defaults to None.
        """
        # Load config
        self.config = config

        # Load the chat LLM
        self.llm = ChatOllama(
            model=model_name,
            base_url=url,
            stop=self.config['stop_tokens']
        )

    def find_experiences(self, job_offer:str):
        """_summary_
        """
        prompt = PromptTemplate.from_template(self.config["experience_filter_prompt"])

        return self.llm.invoke(prompt.format(job_offer=job_offer))
    def find_softskills(self, job_offer:str):
        """_summary_
        """
        prompt = PromptTemplate.from_template(self.config["softskills_filter_prompt"])

        return self.llm.invoke(prompt.format(job_offer=job_offer))
