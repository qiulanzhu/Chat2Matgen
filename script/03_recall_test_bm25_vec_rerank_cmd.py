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

    if len(sys.argv) < 2:
        print("请输入问题。 Usage: python 04_recall_test_bm25_vec_rerank_cmd.py '问题'")
        exit(1)

    question = sys.argv[1]
    doc_list, filename_list = send_request(question)
    print(f"问题: {question}")
    print(f"内容：{doc_list}")
    print(f"文档: {filename_list}")
    print("=" * 50)
