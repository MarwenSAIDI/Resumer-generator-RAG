from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
import yaml

def load_config(config_file:str):
    # Load configs
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config

class RAG_Chain:

    def __init__(self, model_name, url, retriever, config):
        # Load config
        self.config = config

        # Load the chat LLM
        self.llm = ChatOllama(
            model=model_name,
            base_url=url,
            stop=self.config['stop_tokens']
        )

        # TODO: Create the chain
        self.chain = None
