import requests
import json
from loguru import logger

chat_url = "http://localhost:11434/api/chat"
generate_url = "http://localhost:11434/api/generate"
# MODEL = "mixtral:latest"
MODEL = "qwen2:7b-instruct"
# MODEL = "phi3:14b"

def llm_chat(query):
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "assistant",
                "content": "Answer the question based on the 'content' first. If the 'content' cannot answer the question, then use the 'reference' to answer the question."
            },
            {
                "role": "user",
                "content": f"{query}"
            }
        ],
        "stream": False
    }

    logger.debug(f"post data:{data}")
    response = requests.post(chat_url, json=data)
    return response.text