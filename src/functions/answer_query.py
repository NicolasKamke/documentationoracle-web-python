from .get_embedding import get_embedding
from .search_index import search_index
from typing import List
import faiss
import logging

logger = logging.getLogger(__name__)

def answer_query(query: str, index: faiss.IndexFlatL2, chunks: List[str], client, k: int = 5) -> str:
    logger.info("Respondendo à pergunta do usuário.")
    query_embedding = get_embedding(query, client)
    indices, distances = search_index(index, query_embedding, k)
    relevant_chunks = [chunks[i] for i in indices]
    context = '\n\n'.join(relevant_chunks)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um chatbot que responde perguntas sobre projetos da empresa."},
                {"role": "system", "content": f"Contexto:\n{context}\n\n"},
                {"role": "user", "content": f"Pergunta: {query}"}
            ],
            temperature=1
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        logger.error(f"Erro ao gerar a resposta: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."