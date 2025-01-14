import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer(r'E:\Desktop\CaiTing\hf-models\all-MiniLM-L6-v2', device='cpu')


def get_scores(answer, docs):
    answer_embedding = model.encode([answer])
    embeddings = model.encode(docs)
    return cosine_similarity(answer_embedding, embeddings)[0]

def run():
    save_list = []
    with open('recall_test_bm25_vec_rerank_docs.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            question = data['Q']
            answer = data['A']
            docs = data['docs']

            scores = get_scores(answer, docs)
            save_list.append({'question': question, 'answer': answer, 'docs': docs,'scores': scores})

    with open('recall_test_bm25_vec_rerank_scores.jsonl', 'w', encoding='utf-8') as f:
        for item in save_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def run_example():
    question = "什么是机器学习？"
    sentences = [
        "机器学习是一门非常有趣的学科。",
        "我喜欢用Python进行编程。",
        "天气很好，适合出去散步。",
        "人工智能正在改变世界。"
    ]
    scores = get_scores(question, sentences)
    print(scores)

if __name__ == '__main__':
    run_example()




