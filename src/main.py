import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict

from functions import load_embeddings, get_github_wiki, split_text_into_chunks, save_embeddings, create_faiss_index, get_embeddings, answer_query, download_repository, read_repository_files

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

load_dotenv()
# Configuração da API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WIKI_RAW_URLS = ["https://raw.githubusercontent.com/wiki/NicolasKamke/myfinance-web-react/Home.md"]
REPOSITORY_URLS = ["https://github.com/NicolasKamke/myfinance-web-react/archive/main.zip"]

def main():
    if not OPENAI_API_KEY:
        logging.error("Chave da API da OpenAI não encontrada. Defina OPENAI_API_KEY no seu arquivo .env.")
        return

    client = OpenAI(api_key=OPENAI_API_KEY, max_retries=5)

    embeddings, chunks, index = load_embeddings()
    if embeddings is None:
        text = ""
        for url in WIKI_RAW_URLS:
            text += get_github_wiki(url)

        for url in REPOSITORY_URLS:
            repo_folder: str = download_repository(url)
            allowed_extensions: List[str] = [".md", ".py", ".js", ".jsx", ".ts", ".json", ".java", ".cs", ".html", ".css", ".yml", ".yaml", ".txt"]
            files: Dict[str, str] = read_repository_files(repo_folder, allowed_extensions)
            for _, content in files.items():
                text += content

        chunks = split_text_into_chunks(text)
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


# Exemplo de uso
if __name__ == "__main__":
    main()