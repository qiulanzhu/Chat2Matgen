import json

fix_list = [
    "mentioned in the text",
    "described in the text",
    "discussed in the text",
    "according to the text"
]

qa_pairs_fixed = []
# 读取qa_for_recall_rate.jsonl, 一行一行地处理
with open('qa_for_recall_rate.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        qa_pair = json.loads(line)
        question = qa_pair['Q']
        for fix in fix_list:
            if fix in question:
                question = question.replace(fix, "")
        qa_pairs_fixed.append({"Q": question, "A": qa_pair['A']})

print(f"Total {len(qa_pairs_fixed)} question-answer pairs generated.")
with open("qa_for_recall_rate_fixed.jsonl", "w") as f:
    for qa_pair in qa_pairs_fixed:
        f.write(json.dumps(qa_pair) + "\n")