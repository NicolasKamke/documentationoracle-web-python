import logging
from typing import List
import re
import tiktoken
from .clear_text import clear_text

logger = logging.getLogger(__name__)



def split_text_into_chunks(text: str, max_chunk_size: int = 5000) -> List[str]:
    logger.info("Dividindo o texto em chunks.")
    text = clear_text(text)
    enc = tiktoken.get_encoding("cl100k_base")  # Codificação padrão usada pelo GPT-3
    tokens = enc.encode(text)
    
    # Dividir os tokens em chunks que respeitem o tamanho máximo
    chunks = []
    current_chunk = []
    
    for token in tokens:
        if len(current_chunk) < max_chunk_size:
            current_chunk.append(token)
        else:
            chunks.append(enc.decode(current_chunk))
            current_chunk = [token]
    
    # Adiciona o último chunk
    if current_chunk:
        chunks.append(enc.decode(current_chunk))
    
    logging.info(f"Total de chunks criados: {len(chunks)}")
    return chunks