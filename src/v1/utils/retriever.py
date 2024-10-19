""" The retriver and the vector store where all the RAG chunks are stored """

from typing import List
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from src.v1.utils.logger import logger

class SectionsRetriever:
    """_summary_
    """
    def __init__(self,model_name:str, url:str) -> None:
        """
        _summary_
        """

        # Load the embedding model
        self.embedder = OllamaEmbeddings(
            model=model_name,
            base_url=url,
        )
        logger.info("retriever - Initialize the embedding model")

    async def create_embedding(self, text):
        """_summary_

        Args:
            query_list (_type_): _description_

        Returns:
            _type_: _description_
        """
        logger.debug("retriever - Processing the text")
        embedding = await self.embedder.aembed_documents([text])
        logger.info("retriever - Sucessfully generated the embedding")
        return zip([text], embedding)
    
    # def create_retriever(self, query_list):
    #     """_summary_

    #     Args:
    #         query_list (_type_): _description_

    #     Returns:
    #         _type_: _description_
    #     """
    #     query_list = [Document(page_content=chunk) for chunk in query_list]

    #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    #     splits = text_splitter.split_documents(query_list)
    #     vectorstore = Chroma.from_documents(documents=splits, embedding=self.embedder)

    #     return vectorstore.as_retriever(search_type="similarity", search_kwargs={'k':2})
    