import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

def read_repository_files(directory: str, allowed_extensions: Optional[List[str]] = None) -> Dict[str, str]:
    """
    Recursively reads all files in a repository directory, filtering by extensions.
    
    Args:
        directory (str): The root directory of the extracted repository.
        allowed_extensions (Optional[List[str]]): A list of allowed file extensions.
    
    Returns:
        Dict[str, str]: A dictionary mapping file paths to their content.
    """
    files_data: Dict[str, str] = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if allowed_extensions and not file.endswith(tuple(allowed_extensions)):
                continue

            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    files_data[full_path] = f.read()
            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
    return files_data