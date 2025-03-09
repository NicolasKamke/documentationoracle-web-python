import logging
import requests

logger = logging.getLogger(__name__)

def get_github_wiki(url):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.text  # Retorna o conteúdo em Markdown
    else:
        logger.error(f"Erro ao acessar a Wiki: {resposta.status_code}")
        return None