from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
import yaml

class SectionsRetriever:

    def __init__(self,model_name:str, url:str, config_file:str) -> None:
        """
        
        """
        # Load configs
        with open(config_file, 'r') as stream:
            self.conf = yaml.safe_load(stream)

        # Load the embedding model
        self.embedder = OllamaEmbeddings(
            model=model_name,
            base_url=url,
        )

        # Load the chat llm for processing
        self.llm = OllamaLLM(
            model=model_name,
            base_url=url,
            stop=self.conf['llm']['stop_tokens']
        )

    
    def process_experience(self, corpus:str):
        pass
    