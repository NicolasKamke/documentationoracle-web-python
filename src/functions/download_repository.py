import os
import io
import requests
import zipfile
import logging

logger = logging.getLogger(__name__)

def download_repository(url: str) -> str:
    """
    Downloads a GitHub repository as a ZIP file and extracts its contents.
    
    Returns:
        str: Path to the extracted repository folder.
    
    Raises:
        Exception: If the repository download fails.
    """
    print("Downloading repository...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download the repository.")

    zipfile_content = zipfile.ZipFile(io.BytesIO(response.content))
    extract_path = "repo_source"
    zipfile_content.extractall(extract_path)
    
    repo_folder = os.path.join(extract_path, os.listdir(extract_path)[0])  # Obtém o nome da pasta extraída
    logger.info(f"Repository extracted to: {repo_folder}")
    return repo_folder