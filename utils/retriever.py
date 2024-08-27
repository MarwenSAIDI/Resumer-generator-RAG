from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
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
        prompt = PromptTemplate.from_template(self.config["llm"]["experience_extraction_prompt"])

        return self.llm.invoke(prompt.format(schema=self.config["llm"]["experience_extraction_schema"], query=corpus))
    
    def reconstruct_experience(self, section_name:str, json_structure:str) -> str:
        prompt = PromptTemplate.from_template(self.config["llm"]["experience_construct_prompt"])

        return self.llm.invoke(prompt.format(json_text=json_structure, section_name=section_name))
    
    def create_retriever(self, query_list):

        query_list = [Document(page_content=chunk) for chunk in query_list]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(query_list)
        vectorstore = Chroma.from_documents(documents=splits, embedding=self.embedder)

        return vectorstore.as_retriever()