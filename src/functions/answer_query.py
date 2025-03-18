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
    context = "\n\n".join([f"Contexto: (distância {dist:.4f}):\n{chunk}" for chunk, dist in zip(relevant_chunks, distances)])
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um chatbot que só responde perguntas sobre projetos da empresa."},
                {"role": "system", "content": context},
                {"role": "user", "content": f"Pergunta: {query}"}
            ],
            temperature=0.5
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        logger.error(f"Erro ao gerar a resposta: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."