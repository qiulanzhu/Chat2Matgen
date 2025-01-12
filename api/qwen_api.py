import os
from openai import OpenAI


def llm_chat(prompt, model="qwen2.5-72b-instruct"):
    client = OpenAI(
        api_key=os.environ['QWEN_API_KEY'],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
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


if __name__ == '__main__':
    llm_chat("""生成三句金句，json格式返回，例如：{"sentences":["xxx","xxx","xxx"]}""")