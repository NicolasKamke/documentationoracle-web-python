import logging
from typing import List
import faiss
import pickle

logger = logging.getLogger(__name__)

def save_embeddings(embeddings: List[List[float]], chunks: List[str], index: faiss.IndexFlatL2,
                    embeddings_file: str = 'embeddings.pkl',
                    chunks_file: str = 'chunks.pkl',
                    index_file: str = 'faiss.index'):
    logger.info("Salvando embeddings, chunks e índice no disco.")
    with open(embeddings_file, 'wb') as f:
        pickle.dump(embeddings, f)
    with open(chunks_file, 'wb') as f:
        pickle.dump(chunks, f)
    faiss.write_index(index, index_file)