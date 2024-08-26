from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
import yaml

class SectionsRetriever:

    def __init__(self,model_name:str, url:str, config_file:str) -> None:
        """
        
        """
        # Load configs
        with open(config_file, 'r') as stream:
            self.config = yaml.safe_load(stream)

        # Load the embedding model
        self.embedder = OllamaEmbeddings(
            model=model_name,
            base_url=url,
        )

        # Load the chat llm for processing
        self.llm = OllamaLLM(
            model=model_name,
            base_url=url,
            stop=self.config['llm']['stop_tokens']
        )

    
    def process_experience(self, corpus:str) -> str:
        # Create the prompt
        prompt = PromptTemplate.from_template(self.config["llm"]["prompt"])

        return self.llm.invoke(prompt.format(schema=self.config["llm"]["experience_schema"], query=corpus))
    