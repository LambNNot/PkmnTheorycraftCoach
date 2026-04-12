import json
from pathlib import Path
# from pkmn_types import getMonoTypeCode, getDualTypeCode

CWD = Path(__file__).resolve().parent

DATA_FILENAME = "pokemonData.json"
DATA_F_PATH = CWD/DATA_FILENAME

OUTPUT_FILENAME = "pkmn_species.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = ["name", "description"]

def getAbility(abilityList: list, id: str) -> str | None:
    if (len(abilityList) < 1):
        raise ValueError(f"Invalid ability list: {abilityList}")
    
    match id:
        case 'one':
            return abilityList[0]
        case 'two':
            return abilityList[1] if len(abilityList) == 3 else None
        case 'hidden':
            return abilityList[-1] if len(abilityList) > 1 else None
        

def getBaseSpecies(name: str) -> str:
    """Extracts name without the hyphen (e.g. Voltorb-Hisui -> Voltorb)"""
    hyphen_index = name.find("-")
    return name if hyphen_index == -1 else name[: hyphen_index]

def getForme(name: str) -> str:
    """Extracts forme from name if possible (e.g. Voltorb-Hisui -> Hisui)"""
    hyphen_index = name.find("-")
    return "Base" if hyphen_index == -1 else name[hyphen_index+1 :]

def getTypeCode(typesList: list) -> int:
    return getMonoTypeCode(typesList[0]) if len(typesList) == 1 else getDualTypeCode(typesList[0], typesList[1])


if __name__ == "__main__":

    with open(DATA_F_PATH) as f:
        speciesData:list[dict] = json.load(f)

    print(len(speciesData))
    print(list(speciesData[0].keys()))
    print(speciesData[0].get('oob').get('dex_number'))
    print(speciesData[0])

    parsed_results = []
    species = {}

    for s in speciesData:
        if s is None or not s.get('isNonstandard') in ["Standard", "NatDex"]:
            continue
        species_name = getBaseSpecies(s.get("name"))
        
        dexNo = (s.get('oob') or {}).get('dex_number', species.get(species_name))
        species.update({species_name : dexNo})
        parsed_results.append(
            {
                "dex_no" : dexNo,
                "species" : species_name,
                "typeCode" : getTypeCode(s.get("types")),
                "forme" : getForme(s.get("name")),
                "ability_one": getAbility(s.get('abilities'), "one"),
                "ability_two": getAbility(s.get('abilities'), "two"),
                "ability_hidden": getAbility(s.get('abilities'), "hidden"),
                "base_hp": s.get("hp"),
                "base_atk": s.get("atk"),
                "base_def": s.get("def"),
                "base_spa": s.get("spa"),
                "base_spd": s.get("spd"),
                "base_spe": s.get("spe"),
                "weight": s.get("weight")
            }
        )

    # print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)

def getSpecies():
    raise NotImplementedError()
    with open(OUTPUT_F_PATH) as f:
        return json.load(f)
    
def getAllSpecies() -> list:
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)

    species = {}

    result = []

    for s in data:
        species.update({s.get("species") : s.get("dex_no")})
        result.append(
            {
                "dex_no": species.get(s.get("species")) if s.get("dex_no") == -1 else s.get("dex_no"),
                "species": s.get("species"),
                "typeCode": s.get("typeCode"),
                "forme": s.get("forme"),
                "ability_one": s.get("ability_one"),
                "ability_two": s.get("ability_two"),
                "ability_hidden": s.get("ability_hidden"),
                "base_hp": s.get("base_hp"),
                "base_atk": s.get("base_atk"),
                "base_def": s.get("base_def"),
                "base_spa": s.get("base_spa"),
                "base_spd": s.get("base_spd"),
                "base_spe": s.get("base_spe"),
                "weight": s.get("weight"),
            }
        )

    return result



