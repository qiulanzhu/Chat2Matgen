import api.matgen_api as matgen_api
import api.openai_api as openai_api
import api.qanything_api as qanything_api
import query_analyse
from loguru import logger
import sys
from prompt import PROMPT_TEMPLATE


def run(query):
    key_information = ''

    mat_id_list = query_analyse.extract_mat_id(query)
    if len(mat_id_list) > 0:
        for id in mat_id_list:
            key_information += f"This Important attribute of {id}: {matgen_api.search_with_mat_id(id)}\n"

    is_professional_question, question_classify, element_list, formula_list, space_group_list = query_analyse.extract_element(query)

    if is_professional_question and question_classify == 1:
        api_result = ''
        for element, formula, space_group in zip(element_list, formula_list, space_group_list):
            logger.info(f"element:{element}, formula:{formula}, space_group:{space_group}")
            api_result += "<material_property>\n"
            api_result += str(matgen_api.search_with_element(element, space_group)) + "\n"
            api_result += "</material_property>\n"

        key_information += api_result
    else:
        key_information += qanything_api.getRelationPaper(query)


    prompt = PROMPT_TEMPLATE.replace('{{question}}', query)
    prompt = prompt.replace('{key_information}', key_information)
    logger.info(f"prompt:{prompt}")

    answer = openai_api.llm_chat(prompt, json_format=False)
    logger.info(f"answer:{answer}")
    return answer

if __name__ == '__main__':
    input_query = "Can you tell me the crystal system of the crystal material with formula 'Si1 Os1' and space group 'Pm-3m'?"
    if len(sys.argv) >= 2:
        input_query = sys.argv[1]
        
    run(input_query)