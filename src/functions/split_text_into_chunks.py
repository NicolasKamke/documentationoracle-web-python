import logging
from typing import List
import re
from .clear_text import clear_text

logger = logging.getLogger(__name__)



def split_text_into_chunks(text: str, max_chunk_size: int = 1000) -> List[str]:
    logger.info("Dividindo o texto em chunks.")
    text = clear_text(text)
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += ' ' + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    logging.info(f"Total de chunks criados: {len(chunks)}")
    return chunks