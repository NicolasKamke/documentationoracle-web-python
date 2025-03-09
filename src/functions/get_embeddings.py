from typing import List
import logging
from .get_embedding import get_embedding

logger = logging.getLogger(__name__)

def get_embeddings(texts: List[str], client, model: str = "text-embedding-3-small") -> List[List[float]]:
    embeddings = []
    logger.info("Gerando embeddings para os chunks.")
    for i, text in enumerate(texts):
        embedding = get_embedding(text, client, model)
        embeddings.append(embedding)
        if (i + 1) % 10 == 0 or (i + 1) == len(texts):
            logger.info(f"Processados {i + 1}/{len(texts)} chunks.")
    return embeddings