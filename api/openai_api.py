import openai
import os

openai.api_key = os.environ['DEEPSEEK_API_KEY']
openai.base_url = "https://api.deepseek.com"

def llm_chat(prompt, model="deepseek-chat", json_format=True):
    if json_format:
        response_format = {
            'type': 'json_object'
        }
    else:
        response_format = {
            'type': 'text'
        }

    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. You are always a reliable assistant that can answer questions with the help of external documents.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format=response_format
    )

    ret = completion.choices[0].message.content
    print(ret)
    print(f'model:{model}')
    return ret

def llm_chat_stream(prompt='hi', model="deepseek-chat"):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. You are always a reliable assistant that can answer questions with the help of external documents.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=True
    )

    for chunk in response:
        content_piece = chunk.choices[0].delta.content
        if content_piece is not None:
            yield content_piece

if __name__ == '__main__':
    for content_piece in  llm_chat_stream("随机生成3句金句", model="deepseek-chat"):
        print(content_piece, end='', flush=True)