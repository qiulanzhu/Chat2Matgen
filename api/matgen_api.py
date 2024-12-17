import matgen_rester as mr
from loguru import logger


def search_with_mat_id(mat_id='mat_16680') -> list[dict]:
    with mr.MatgenRester(username="matgen", password="true") as q:
        structure_list = q.get_structure_by_id(targetId=mat_id,
                                          idType="matid",
                                          fields=[
                                              "structure.matid",
                                              "structure.formula",
                                              "structure.crystal_system",
                                              "structure.point_group",
                                              "structure.spacegroup",
                                              "structure.density"
                                          ])
        logger.info(f"{mat_id} infomation:{structure_list}")
        return structure_list


def search_with_element(elements, space_group) -> list[dict]:
    with mr.MatgenRester(username="matgen", password="true") as q:
        structure_list = q.get_structure_with_filter(filter={
            "in": '-'.join(elements),
            "searchType": "only",
            "crystalSystem": [
                "cubic", "triclinic", "hexagonal", "trigonal", "tetragonal", "monoclinic", "orthorhombic", 
            ],
            "pointGroup": ["3", "-6", "222", "23", "-6m2", "4mm", "-1", "4/m", "m-3", "432", "6/mmm", "2", "622", "3m", "-43m", 
                           "32", "6/m", "4", "m", "1", "4/mmm", "-3", "mmm", "-3m", "6mm", "6", "422", "mm2", "-42m", "m-3m", "2/m", 
                           "-4"

            ],
            "spaceGroup": [space_group],
        }, fields=[
            "structure.matid",
            "structure.formula",
            "structure.crystal_system",
            "structure.point_group",
            "structure.spacegroup",
            "structure.density"],
            size=50,
            page=0)

        logger.info(structure_list)

    return structure_list


if __name__ == "__main__":
    # search_with_mat_id()
    search_with_element(['Si', 'Os'], 'Pm-3m')
