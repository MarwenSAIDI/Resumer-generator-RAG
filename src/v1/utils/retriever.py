""" The retriver and the vector store where all the RAG chunks are stored """

from typing import List
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
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
        self.retriever = None
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
    
    def set_retriever(self, text_embedding_pairs, k) -> None:
        """_summary_

        Args:
            text_embedding_pairs (_type_): _description_
        """

        logger.debug("retriever - Initialize the retriever object")
        vectorstore = None
        for i, pair in enumerate(text_embedding_pairs):
            if i == 0:
                vectorstore = FAISS.from_embeddings(pair, self.embedder)
            else:
                vectorstore.merge_from(FAISS.from_embeddings(pair, self.embedder))
            logger.info("retriever - Added retriever object")

        

        self.retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k':k})
        logger.info("retriever - Sucessfully created the retriever object")

    async def get_relevant_experiences(self, job_offer: str) -> None:
        """_summary_

        Args:
            job_offer (str): _description_
        """
        exps = await self.retriever.ainvoke(job_offer)

        return [e.page_content for e in exps]
    