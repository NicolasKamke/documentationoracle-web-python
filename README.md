# IA Generativa - Documentation Oracle

Este projeto é uma aplicação Python que utiliza a API da OpenAI para gerar embeddings de texto e realizar buscas semânticas em um índice FAISS. A aplicação carrega textos de uma wiki do GitHub, divide o texto em chunks, gera embeddings para esses chunks e os armazena em arquivos locais. A aplicação também permite que o usuário faça perguntas e obtenha respostas baseadas nos textos indexados.

## Estrutura do Projeto

```
.env
.gitignore
chunks.pkl
embeddings.pkl
faiss.index
LICENSE
README.md
requirements.txt
src/
    functions/
        __init__.py
        answer_query.py
        clear_text.py
        create_faiss_index.py
        get_embedding.py
        get_embeddings.py
        get_github_wiki.py
        load_embeddings.py
        save_embeddings.py
        search_index.py
        split_text_into_chunks.py
    main.py
venv/
    Include/
    Lib/
        site-packages/
    pyvenv.cfg
    Scripts/
        activate
        activate.bat
        Activate.ps1
        deactivate.bat
        distro.exe
        dotenv.exe
```

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Crie um arquivo .env na raiz do projeto e adicione sua chave da API da OpenAI:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Uso

Para executar a aplicação, utilize o seguinte comando:

```
python src/main.py
```

A aplicação irá carregar os embeddings e chunks dos arquivos locais, se existirem. Caso contrário, irá buscar o texto da wiki do GitHub, dividir o texto em chunks, gerar embeddings e salvar esses dados em arquivos locais.

### Exemplo de Uso

Após iniciar a aplicação, você pode digitar perguntas no console. Para sair, digite `sair`.

```
Digite sua pergunta (ou 'sair' para terminar):
>> O que é IA Generativa?
Resposta:
 IA Generativa é um campo da inteligência artificial que se concentra na criação de novos conteúdos, como texto, imagens, música, etc., utilizando modelos de aprendizado de máquina.
```


## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

* Nícolas Kamke Schimidt: 206997
