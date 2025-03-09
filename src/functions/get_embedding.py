from typing import List
import logging

logger = logging.getLogger(__name__)

def get_embedding(text: str, client, model: str = "text-embedding-3-small") -> List[float]:
    text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(input=[text], model=model)
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        logger.error(f"Erro ao obter embedding para o texto: {e}")
        return []