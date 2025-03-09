import os
import re
import logging
from dotenv import load_dotenv
from openai import OpenAI
import faiss
from typing import List
import requests
import numpy as np
import pickle

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

load_dotenv()
# Configuração da API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WIKI_RAW_URL = "https://raw.githubusercontent.com/wiki/NicolasKamke/myfinance-web-react/Home.md"

def main():
    if not OPENAI_API_KEY:
        logging.error("Chave da API da OpenAI não encontrada. Defina OPENAI_API_KEY no seu arquivo .env.")
        return

    client = OpenAI(api_key=OPENAI_API_KEY, max_retries=5)

    embeddings, chunks, index = load_embeddings()
    if embeddings is None:
        wiki_text = get_github_wiki(WIKI_RAW_URL)
        chunks = split_text_into_chunks(wiki_text)
        embeddings = get_embeddings(chunks, client)
        index = create_faiss_index(embeddings)
        save_embeddings(embeddings, chunks, index)
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

def get_github_wiki(url):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.text  # Retorna o conteúdo em Markdown
    else:
        logging.error(f"Erro ao acessar a Wiki: {resposta.status_code}")
        return None

def split_text_into_chunks(text: str, max_chunk_size: int = 5000) -> List[str]:
    logging.info("Dividindo o texto em chunks.")
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

def save_embeddings(embeddings: List[List[float]], chunks: List[str], index: faiss.IndexFlatL2,
                    embeddings_file: str = 'embeddings.pkl',
                    chunks_file: str = 'chunks.pkl',
                    index_file: str = 'faiss.index'):
    logging.info("Salvando embeddings, chunks e índice no disco.")
    with open(embeddings_file, 'wb') as f:
        pickle.dump(embeddings, f)
    with open(chunks_file, 'wb') as f:
        pickle.dump(chunks, f)
    faiss.write_index(index, index_file)

def create_faiss_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    logging.info("Criando índice FAISS.")
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index

def get_embeddings(texts: List[str], client, model: str = "text-embedding-3-small") -> List[List[float]]:
    embeddings = []
    logging.info("Gerando embeddings para os chunks.")
    for i, text in enumerate(texts):
        embedding = get_embedding(text, client, model)
        embeddings.append(embedding)
        if (i + 1) % 10 == 0 or (i + 1) == len(texts):
            logging.info(f"Processados {i + 1}/{len(texts)} chunks.")
    return embeddings

def get_embedding(text: str, client, model: str = "text-embedding-3-small") -> List[float]:
    text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(input=[text], model=model)
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        logging.error(f"Erro ao obter embedding para o texto: {e}")
        return []

def answer_query(query: str, index: faiss.IndexFlatL2, chunks: List[str], client, k: int = 5) -> str:
    logging.info("Respondendo à pergunta do usuário.")
    query_embedding = get_embedding(query, client)
    indices, distances = search_index(index, query_embedding, k)
    relevant_chunks = [chunks[i] for i in indices]
    context = '\n\n'.join(relevant_chunks)
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

def search_index(index: faiss.IndexFlatL2, query_embedding: List[float], k: int = 5):
    logging.info("Pesquisando no índice FAISS por embeddings similares.")
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    return indices[0], distances[0]


# Exemplo de uso
if __name__ == "__main__":
    main()