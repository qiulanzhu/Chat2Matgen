from openai import OpenAI
import uuid
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")
conversations = {}

def chat_stream(conversation_id, user_input):
    if conversation_id not in conversations:
        conversations[conversation_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    conversations[conversation_id].append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=conversations[conversation_id],
            stream=True
        )

        full_reply = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content_piece = chunk.choices[0].delta.content
                full_reply += content_piece
                yield content_piece

        conversations[conversation_id].append({"role": "assistant", "content": full_reply})
    except Exception as e:
        yield f"Error: {str(e)}"

if __name__ == '__main__':
    conversation_id = str(uuid.uuid4())
    print(f"Generated Conversation ID: {conversation_id}")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        print("Assistant: ", end="", flush=True)
        for output in chat_stream(conversation_id, user_input):
            print(output, end="", flush=True)
        print()
