import re
from loguru import logger
import json
import api.openai_api as openai_api
import api.qwen_api as qwen_api
import traceback

def extract_mat_id(query):
    mat_id_list = []
    matches = re.findall(r'mat_\d+', query)
    for match in matches:
        logger.info(match)
        mat_id_list.append(match)
    return mat_id_list


def extract_element(query):
    prompt = """
    <text>{query}</text>
    你是一个专业的材料科学信息提取助手。你的任务是从给定的文本中精确提取材料科学相关的结构信息。
    提取规则:
    1. 严格检查输入是否为材料科学专业查询
    2. 严格检查输入属于下面的哪一类：
     - 0：其它
     - 1：查询材料属性类问题(属性包括crystal system、point group、space group、density等)
     - 2：查询材料相关的知识理解问题
    3. 按照以下标准提取关键信息:
     - 化学式: 识别并分离每个元素
     - 空间群: 提取精确的空间群符号
    输出JSON格式要求:
    {
      "is_professional_question": 布尔值,
      "question_classify": 0、1、2三种分类中的其中一类,
      "formula": {
        "elements": [["元素1", "元素2", ...], ...],
        "stoichiometry": [{
          "元素1": 数量,
          "元素2": 数量,
          ...
        }, ...]
      },
      "space_group": ["空间群1", ...],
      "confidence_score": 0-1之间的数值
    }
    特殊处理说明:
    - 如无法识别,相应字段返回null
    示例输入1: What is the crystal system of the crystal material with formula "Nd1 Al3 Ni2" and space group "P6/mmm"?
    示例输出1: {
      "is_professional_question": true,
      "question_classify": 1,
      "formula": {
        "elements": [["Nd", "Al", "Ni"]],
        "stoichiometry": [{
          "Nd": 1,
          "Al": 3, 
          "Ni": 2
        }]
      },
      "space_group": ["P6/mmm"],
      "confidence_score": 0.95
    }
    注意，由于存在多个化学表达的情况，因此formula的elements和stoichiometry为数组类型。
    请根据上述规则,准确、详细地提取材料科学信息。
    """
    prompt = prompt.replace('{query}', query)
    logger.info(prompt)
    try:
        data = json.loads(qwen_api.llm_chat(prompt))
        logger.info(data)

        formula_list = []
        if data['formula'] and data['formula']['elements'] and data['formula']['stoichiometry']:
            for i, elements in enumerate(data['formula']['elements']):
                formula = ''
                for element in elements:
                    formula += element + str(data['formula']['stoichiometry'][i][element]) + ' '
                formula_list.append(formula.strip())

        space_group_list = [None]
        if data['space_group']:
            space_group_list = data['space_group']

        elements_list = [None]
        if data['formula']['elements']:
            elements_list = data['formula']['elements']

        return data['is_professional_question'], data['question_classify'], elements_list, formula_list, space_group_list
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return None, None, None, None, None

if __name__ == "__main__":
    # 提取mat_id，查询晶体材料属性
    query = 'Tell me the energy of materials mat_333 and mat_444?'
    extract_mat_id(query)

    # 提取元素，查询晶体材料列表(用LLM提取)
    query = "What is the density of the crystal material with formula 'Si1 Os1' and space group 'Pm-3m'?"
    ret = extract_element(query)
    logger.info(ret)
