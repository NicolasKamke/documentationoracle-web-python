import re

def clear_text(text):
    """Remove caracteres especiais desnecessários e normaliza espaços."""
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)  # Remove links Markdown
    text = re.sub(r"\s+", " ", text).strip()  # Remove múltiplos espaços
    return text