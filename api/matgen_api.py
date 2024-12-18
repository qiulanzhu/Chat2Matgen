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
    if elements is None and space_group is None:
        return []

    if space_group is None:
        space_group = ["Pm-3m", "P312", "P3_121", "P-42m", "I-42d", "Pmna", "Pn-3n", "P3_221", "P-3", "P-4c2", "Imm2", "Pmma", "P6_122", "Pc", "I4_1cd", "I4/mcm", "I-42m", "P2_13", "P4/mmm", "Cccm", "P-3m1", "I4_1/acd", "P4/mbm", "Fddd", "Fm-3c", "Immm", "P-43n", "I23", "P6_3", "P2_1", "P-4", "Ia-3d", "Aea2", "Pbca", "P4nc", "P6_1", "P6_4", "P4_32_12", "I-4", "Pbcm", "Pbam", "P6_422", "P6/mcc", "P23", "Pban", "P-6", "Pn-3", "Pnn2", "I4_1/a", "P4_2/ncm", "P6mm", "P4/n", "Pccn", "C2/m", "Pnnn", "P-43m", "R3c", "Ibam", "P6_222", "I4_132", "I432", "F222", "C222_1", "R-3", "P2/c", "Ccce", "Iba2", "Pm", "Fdd2", "C2/c", "P4_3", "P6_5", "I-43m", "P4_2/mmc", "P-42_1c", "C222", "P4_2/m", "Pn-3m", "P4bm", "P-42c", "P6cc", "Fd-3m", "Pnc2", "P4_232", "R32", "P422", "Pnnm", "Pma2", "P3m1", "I422", "Fd-3", "I4_1/amd", "I2_12_12_1", "P4mm", "P3_112", "P4_2/nbc", "I-4m2", "I4cm", "P-6c2", "P4/ncc", "P2_12_12_1", "P6_3/m", "R-3c", "P-62c", "F23", "F-43c", "Pnma", "C2", "P2", "I4", "Pmm2", "P4cc", "P6_3cm", "P4_132", "Cmcm", "P4/mcc", "R-3m", "Pba2", "P42_12", "P4_2/nmc", "I4_1md", "Pmc2_1", "P4_322", "Ima2", "P2/m", "P2_12_12", "P31m", "P-3c1", "P3_1", "P6_3/mmc", "Pcc2", "Cmce", "Fm-3", "Pccm", "F4_132", "I-43d", "P-4m2", "R3m", "Pcca", "Fmm2", "I222", "R3", "Imma", "I-4c2", "Ia-3", "Fd-3c", "P4/mnc", "Cc", "Pnna", "Amm2", "P6_3mc", "P622", "P-4n2", "P4/nmm", "I2_13", "P3c1", "P-31c", "P6_2", "P4", "Pca2_1", "Fmmm", "P4_2", "P4_2mc", "P4/nnc", "P2_1/m", "P2_1/c", "Pmn2_1", "Cmc2_1", "Ibca", "I4_1", "P1", "P6/mmm", "P4_332", "Im-3m", "Pna2_1", "P4_2bc", "P321", "P3", "Pbcn", "P4_122", "Cmm2", "P4_2/mbc", "P4_2nm", "Cm", "P4_2cm", "P222", "P4_2/mnm", "Ama2", "P-62m", "I4/m", "P6/m", "I4/mmm", "P4_2/n", "F-43m", "P6_3/mcm", "P4/nbm", "P4_12_12", "P-6m2", "Cmme", "Aem2", "Pa-3", "P4/m", "P31c", "P-4b2", "Cmmm", "P222_1", "P6_322", "P3_2", "P6", "P4_1", "Pmmm", "P4_2/nnm", "Ccc2", "Fm-3m", "P-31m", "I4mm", "Im-3", "Pm-3n", "P-1", "P4_22_12", "P4_2/mcm", "Pm-3", "I4_122", "Pmmn", "P-42_1m"]
    else:
        space_group = [space_group]

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
            "spaceGroup": space_group,
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
    # search_with_element(['Si', 'Os'], 'Pm-3m')
    search_with_element(['Na', 'Cl'], None)
