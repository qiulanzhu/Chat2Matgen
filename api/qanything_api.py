import sys
import requests
import time
import traceback

def getRelationPaper(query):
    url = 'http://127.0.0.1:8777/api/local_doc_qa/local_doc_chat'
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "user_id": "zzp",
        "kb_ids": ["KB22fcb8bff6ae4c3cb851731b16c88249"],
        "question": f"{query}",
    }
    try:
        response = requests.post(url=url, headers=headers, json=data, timeout=60)
        res = response.json()

        contents = []
        for document in res['source_documents']:
            contents.append(document['content'])

        return contents[0:5]
    except Exception as e:
        print(f"请求发送失败: {e}")
        traceback.print_exc()
        return []


if __name__ == '__main__':
    ret = getRelationPaper("what is One-Pot?")
    print(ret)
    print(f"len={len(ret)}")
