import sys

import requests
import json

def send_request(question):
    url = 'http://127.0.0.1:8777/api/local_doc_qa/local_doc_chat'
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "user_id": "zzp",
        "kb_ids": ["KBa3ed65890df842fcb8e2f9f9392f3ac7"],
        "history": [],
        "question": question,
        "rerank": True,
    }
    try:
        response = requests.post(url=url, headers=headers, json=data, timeout=60)
        res = response.json()
        doc_list = []
        filename_list = []
        for doc in res['source_documents']:
            doc_list.append(doc['content'])
            filename_list.append(doc['file_name'])

        return doc_list, filename_list
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

    bm25_vec_rerank_docs = []
    for question, answer in qa_list[0:3]:
        doc_list, filename_list = send_request(question)
        bm25_vec_rerank_docs.append({"Q": question, "A": answer, "docs": doc_list})

    with open('recall_test_vec.jsonl', 'w', encoding='utf-8') as f:
        for doc in bm25_vec_rerank_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')