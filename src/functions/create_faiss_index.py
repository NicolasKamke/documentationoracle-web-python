import logging
from typing import List
import faiss
import numpy as np

logger = logging.getLogger(__name__)

def create_faiss_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    logger.info("Criando índice FAISS.")
    dimension = len(embeddings[0])
    logger.info(f"Embedding dimension: {dimension}") 
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index