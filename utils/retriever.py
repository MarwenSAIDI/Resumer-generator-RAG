""" The retriver and the vector store where all the RAG chunks are stored """

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class SectionsRetriever:
    """_summary_
    """
    def __init__(self,model_name:str, url:str, config_retriever) -> None:
        """
        
        """
        # Load configs
        self.config = config_retriever

        # Load the embedding model
        self.embedder = OllamaEmbeddings(
            model=model_name,
            base_url=url,
        )

        # Load the chat llm for processing
        self.llm = ChatOllama(
            model=model_name,
            base_url=url,
            stop=self.config['stop_tokens']
        )
    def process_experience(self, corpus:str) -> str:
        """_summary_

        Args:
            corpus (str): _description_

        Returns:
            str: _description_
        """
        # Create the prompt
        prompt = PromptTemplate.from_template(self.config["experience_extraction_prompt"])
        schema = self.config["experience_extraction_schema"]
        query = prompt.format(schema=schema, query=corpus)

        return self.llm.invoke(query)
    def reconstruct_experience(self, section_name:str, json_structure:str) -> str:
        """_summary_

        Args:
            section_name (str): _description_
            json_structure (str): _description_

        Returns:
            str: _description_
        """
        prompt = PromptTemplate.from_template(self.config["experience_construct_prompt"])

        return self.llm.invoke(prompt.format(json_text=json_structure, section_name=section_name))
    def create_retriever(self, query_list):
        """_summary_

        Args:
            query_list (_type_): _description_

        Returns:
            _type_: _description_
        """
        query_list = [Document(page_content=chunk) for chunk in query_list]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(query_list)
        vectorstore = Chroma.from_documents(documents=splits, embedding=self.embedder)

        return vectorstore.as_retriever(search_type="similarity", search_kwargs={'k':2})
    