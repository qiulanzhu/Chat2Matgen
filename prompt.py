INSTRUCTIONS = """
- Answer the question strictly based on the reference information provided between <KEY_INFORMATION> and </KEY_INFORMATION>. 
- Do not attempt to modify or adapt unrelated information. If the reference information does not match the person or topic mentioned in the question, respond only with: \"抱歉，检索到的参考信息并未提供任何相关的信息，因此无法回答。\"
- Before generating the answer, please confirm the following (Let's think step by step):
    1. First, check if the reference information directly matches the person or topic mentioned in the question. If no match is found, immediately return: \"抱歉，检索到的参考信息并未提供任何相关的信息，因此无法回答。\"
    2. If a match is found, ensure all required key points or pieces of information from the reference are addressed in the answer.
- Now, answer the following question based on the above retrieved documents:
{{question}}
- Please format your response in a **logical and structured manner** that best fits the question. Follow these guidelines:

    1. **Start with a concise and direct answer to the main question**.

    2. **If necessary, provide additional details** in a structured format:
       - Use **appropriate multi-level headings (##, ###, ####)** to separate different parts or aspects of the answer.
       - **Use bullet points (-, *) or numbered lists (1., 2., 3.)** if multiple points need to be highlighted.
       - **Highlight key information using bold or italic text** where necessary.

    3. **Tailor the format to the nature of the question**. For example:
       - If the question involves a list or comparison, use bullet points or tables.
       - If the question requires a more narrative answer, structure the response into clear paragraphs.

    4. **Avoid unnecessary or irrelevant sections**. Focus solely on presenting the required information in a clear, concise, and well-structured manner.
- Respond in the same language as the question "{{question}}".
"""
"""
- Please format your response in Markdown with a clear and complete structure:
    1. **Introduction**: Briefly and directly answer the main question.
    2. **Detailed Explanation** (if more relevant details are available):
       - Use **second-level headings (##)** to separate different parts or aspects of the answer.
       - Use **ordered lists** (1., 2.,3.) or **unordered lists** (-, *) to list multiple points or steps.
       - Highlight key information using **bold** or *italic* text where appropriate.
       - If the answer is extensive, conclude with a **brief summary**.
    3. **Notes**:
       - Respond in the **same language** as the question "{{question}}".
       - Avoid including irrelevant information; ensure the answer is related to the retrieved reference information.
       - Ensure the answer is well-structured and easy to understand.
"""

PROMPT_TEMPLATE = f"""
<INSTRUCTIONS>
{INSTRUCTIONS}
</INSTRUCTIONS>

<KEY_INFORMATION>
{{key_information}}
</KEY_INFORMATION>
"""