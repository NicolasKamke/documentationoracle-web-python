import os
import logging
import pickle
import faiss

logger = logging.getLogger(__name__)

def load_embeddings(embeddings_file: str = 'embeddings.pkl',
                    chunks_file: str = 'chunks.pkl',
                    index_file: str = 'faiss.index'):
    if os.path.exists(embeddings_file) and os.path.exists(chunks_file) and os.path.exists(index_file):
        logger.info("Carregando embeddings, chunks e índice do disco.")
        with open(embeddings_file, 'rb') as f:
            embeddings = pickle.load(f)
        with open(chunks_file, 'rb') as f:
            chunks = pickle.load(f)
        index = faiss.read_index(index_file)
        return embeddings, chunks, index
    else:
        logger.warning("Arquivos de embeddings não encontrados.")
        return None, None, None