import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
import faiss
from typing import List

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

load_dotenv()
# Configuração da API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    if not OPENAI_API_KEY:
        logging.error("Chave da API da OpenAI não encontrada. Defina OPENAI_API_KEY no seu arquivo .env.")
        return

    client = OpenAI(api_key=OPENAI_API_KEY, max_retries=5)

    embeddings, chunks, index = load_embeddings()
    if embeddings is None:
        logging.info("Embeddings não carregados dos arquivos.")
    else:
        logging.info("Embeddings carregados dos arquivos.")
    
        print("Digite sua pergunta (ou 'sair' para terminar):")

    while True:
        query = input(">> ")
        if query.lower() == 'sair':
            break
        answer = answer_query(query, index, chunks, client)
        print("\nResposta:\n", answer)

    # pergunta = input("Digite sua pergunta: ")
    # resposta = perguntar_gpt4(pergunta)
    # print("\nResposta do GPT-4:\n", resposta)

def load_embeddings():
    return None, None, None
    

def answer_query(query: str, index: faiss.IndexFlatL2, chunks: List[str], client, k: int = 5) -> str:
    logging.info("Respondendo à pergunta do usuário.")
    # query_embedding = get_embedding(query, client)
    # indices, distances = search_index(index, query_embedding, k)
    # relevant_chunks = [chunks[i] for i in indices]
    # context = '\n\n'.join(relevant_chunks)
    context = ""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um chatbot que responde perguntas sobre documentação de sistemas."},
                {"role": "system", "content": "Contexto:\n{context}\n\n"},
                {"role": "user", "content": f"Pergunta: {query}"}
            ],
            temperature=1
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        logging.error(f"Erro ao gerar a resposta: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."


# Exemplo de uso
if __name__ == "__main__":
    main()