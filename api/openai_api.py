from openai import OpenAI
import openai
import os

client = OpenAI(api_key="sk-wpxmcurxrehxghluhgrvsebfqmgizoguobvejimfeucegyno", base_url="https://api.siliconflow.cn/v1")

def llm_chat(prompt, model="deepseek-ai/DeepSeek-V3", json_format=False):
    if json_format:
        response_format = {
            'type': 'json_object'
        }
    else:
        response_format = {
            'type': 'text'
        }

    response = client.chat.completions.create(
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

    ret = response.choices[0].message.content
    print(ret)
    print(f'model:{model}')
    ret = ret.replace("""```json""", "")
    ret = ret.replace("""```""", "")
    return ret

def llm_chat_stream(prompt='hi', model="deepseek-ai/DeepSeek-V3"):
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )

    for chunk in response:
        content_piece = chunk.choices[0].delta.content
        if content_piece is not None:
            yield content_piece

if __name__ == '__main__':
    # for content_piece in  llm_chat_stream("随机生成3句金句", model="deepseek-ai/DeepSeek-V3"):
    #     print(content_piece, end='', flush=True)

    llm_chat("""随机生成3句金句，返回格式{"sentences": ["xxx", "xxx", "xxx"]}""", json_format=False)