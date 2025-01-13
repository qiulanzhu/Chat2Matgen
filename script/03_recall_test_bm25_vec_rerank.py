import requests
import json

def send_request(question):
    url = 'http://127.0.0.1:8777/api/local_doc_qa/local_doc_chat'
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "user_id": "zzp",
        "kb_ids": ["KBf42f9bab99fa4ebd93a59be1e42f1969"],
        "history": [],
        "question": question,
        "rerank": True,
    }
    try:
        response = requests.post(url=url, headers=headers, json=data, timeout=60)
        res = response.json()
        doc_list = []
        for doc in res['source_documents']:
            content = doc['content']
            doc_list.append(content)

        return doc_list
    except Exception as e:
        print(f"请求发送失败: {e}")

if __name__ == '__main__':
    qa_list = []
    with open('qa_for_recall_rate_fixed.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            question = data['Q']
            answer = data['A']
            qa_list.append((question, answer))

    for question, answer in qa_list[0:3]:
        docs = send_request(question)
        print(f"问题: {question}")
        print(f"答案: {answer}")
        print(f"文档: {docs}")
        print("="*50)
