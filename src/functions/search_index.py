from typing import List
import faiss
import logging
import numpy as np

logger = logging.getLogger(__name__)

def search_index(index: faiss.IndexFlatL2, query_embedding: List[float], k: int = 5):
    logger.info("Pesquisando no índice FAISS por embeddings similares.")
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    return indices[0], distances[0]