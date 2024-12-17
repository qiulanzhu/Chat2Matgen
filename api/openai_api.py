import openai
import os

def llm_chat(prompt, model="deepseek-chat", json_format=True):
    openai.api_key = os.environ['DEEPSEEK_API_KEY']
    openai.base_url = "https://api.deepseek.com"

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

if __name__ == '__main__':
    llm_chat("""随机生成一句金句""", model="deepseek-chat", json_format=False)