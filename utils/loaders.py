""" Build the loaders for the main LLM and the config file """

from langchain_ollama.chat_models import ChatOllama
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

    def __init__(self, model_name:str, url:str, config, retriever=None) -> None:
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

        self.retriever = retriever
    def call_chain(self):
        """_summary_
        """
        return 0
    def format_resumer(self):
        """_summary_
        """
        return 0
