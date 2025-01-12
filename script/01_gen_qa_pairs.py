import json
import os
from PyPDF2 import PdfReader
from api.openai_api import llm_chat
from tqdm import tqdm

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        full_text = ""
        
        # 将所有页面内容合并
        for page in reader.pages:
            full_text += page.extract_text()

        # print(full_text)
        return full_text
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

# 指定数据目录
data_dir = "data"

prompt_template_for_doc = """
<THESIS>
    [thesis]
</THESIS>

<INSTRUCTION>
请根据上面的论文，提取论文的两个片段。
 - 一个结论片段
 - 一个创新点片段
 - 每个片段大约200-500字符
 - 片段来自论文的某个连续部分，不要改写
回答格式采用json格式：
{"Q":["xxx", "xxx"]}
</INSTRUCTION>

注意：
 - 用英文回答。
"""

prompt_template_for_question = """
<DOC>
    [doc]
</DOC>

<INSTRUCTION>
请根据上面的论文片段，写1个问题。
 - 问题是针对该论文片段进行提问。
 - 问题简单直接，不涉及复杂的推理。
 - 问题要放到一个问题库中，对多篇论文进行提问，所有不要出现in the paper这样的提问方式。
 - 论文片段要能够很明显地回答这个问题，让小学生看了论文片段也能回答这个问题。
回答格式采用json格式：
{"Q":"xxx"}
</INSTRUCTION>

注意：
 - 用英文回答。
"""

qa_pairs = []

for filename in tqdm(os.listdir(data_dir)):
    if filename.endswith(".pdf"):
        file_path = os.path.join(data_dir, filename)
        
        content = read_pdf(file_path)
        prompt = prompt_template_for_doc.replace("[thesis]", content)
        docs_str = llm_chat(prompt)
        json_docs = json.loads(docs_str)
        docs = json_docs["Q"]
        for doc in docs:
            prompt = prompt_template_for_question.replace("[doc]", doc)
            question_str = llm_chat(prompt)
            json_question = json.loads(question_str)
            question = json_question["Q"]
            qa_pairs.append({"Q": question, "A": doc})

print(f"Total {len(qa_pairs)} question-answer pairs generated.")
with open("qa_for_recall_rate.jsonl", "w") as f:
    for qa_pair in qa_pairs:
        f.write(json.dumps(qa_pair) + "\n")