import os
from openai import OpenAI

QWEN_API_KEY = os.getenv("QY_QWEN_API_KEY")
client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def llm_chat(prompt, model="qwen2.5-72b-instruct"):
    completion = client.chat.completions.create(
        model="qwen2.5-72b-instruct",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ],
        response_format={"type": "json_object"}
    )

    ret = completion.choices[0].message.content
    print(ret)
    print(f'model: {model}')
    return ret

def llm_chat_stream(prompt='hi', model="deepseek-ai/DeepSeek-V3"):
    response = client.chat.completions.create(
        model="qwen2.5-72b-instruct",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ],
        stream=True
    )

    for chunk in response:
        content_piece = chunk.choices[0].delta.content
        if content_piece is not None:
            yield content_piece

if __name__ == '__main__':
    llm_chat("""生成三句金句，json格式返回，例如：{"sentences":["xxx","xxx","xxx"]}""")