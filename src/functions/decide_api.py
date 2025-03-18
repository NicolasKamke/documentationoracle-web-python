import logging
from typing import List
import faiss
import numpy as np
from .get_embedding import get_embedding
from .search_index import search_index
from typing import Dict
import json
import re

logger = logging.getLogger(__name__)

def decide_api(query: str, index: faiss.IndexFlatL2, chunks: List[str], client, k: int = 5) -> Dict:
    """
    Uses AI to decide which API to use and what parameters to pass.
    """

    query_embedding = get_embedding(query, client)
    indices, distances = search_index(index, query_embedding, k)
    relevant_chunks = [chunks[i] for i in indices]
    context = "\n\n".join([f"Context (distance {dist:.4f}):\n{chunk}" for chunk, dist in zip(relevant_chunks, distances)])
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente que encontra a API correta para chamar com base na documentação do sistema. Caso a consulta envolva uma ação específica, retorne um objeto JSON com 'api' (nome da API), 'endpoint' (IP + PORTA + PATH), 'method' (GET/POST) e 'params' (parâmetros). Caso contrário, retorne 'None'."},
                {"role": "system", "content": "Os tipos das propriedades devem ser: 'api': 'string', 'endpoint': 'string', 'method': 'string', 'params': 'dictionary'. Se não for possível, retorne 'None'."},
                {"role": "system", "content": "Não deve retornar arrays para 'api', 'endpoint', 'method' ou 'params'. Caso contrário, retorne 'None'."},
                {"role": "system", "content": "Somente retorne um objeto com 'api', 'endpoint', 'method' e 'params' se a consulta envolver uma ação específica. Se a consulta for muito genérica (ex.: 'Liste os endpoints'), retorne 'None'."},
                {"role": "system", "content": "Se a consulta envolver parâmetros como datas ou filtros específicos, retorne o objeto que corresponda à ação de consulta relacionada."},
                {"role": "system", "content": f"Documentação da API:\n{context}"},
                {"role": "user", "content": f"Pergunta '{query}'"}
            ],
            temperature=0.5
        )
        decision = response.choices[0].message.content

        if decision == "None":
            return None
        
        match = re.search(r"```json\n(.*?)\n```", decision, re.DOTALL)
    
        if match:
            json_str = match.group(1).strip()  # Remove espaços extras
            return eval(json_str)

        return None  # Converts JSON string to dictionary
    except Exception as e:
        logger.error(f"Error deciding API: {e}")
        return {"api": None}