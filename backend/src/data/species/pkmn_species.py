import json
from pathlib import Path

CWD = Path(__file__).resolve().parent
DATA_FILENAME = "pokemonData.json"
DATA_F_PATH = CWD/DATA_FILENAME

OUTPUT_FILENAME = "pkmn_species.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = ["name", "description"]

if __name__ == "__main__":

    with open(DATA_F_PATH) as f:
        speciesData:list[dict] = json.load(f)

    print(len(speciesData))
    print(list(speciesData[0].keys()))
    print(speciesData[0].get('oob').get('dex_number'))
    print(speciesData[0])

    parsed_results = [
        {
            "dex_no" : (s.get('oob') or {}).get('dex_number', -1),
            "species" : s.get("name"),
            "typeCode" : -1,
            "forme" : "None",
            "ability_one_id": -1,
            "ability_two_id": -2,
            "base_hp": s.get("hp"),
            "base_atk": s.get("atk"),
            "base_def": s.get("def"),
            "base_spa": s.get("spa"),
            "base_spd": s.get("spd"),
            "base_spe": s.get("spe"),
            "weight": s.get("weight")
        }
        for s in speciesData if s is not None and s.get('isNonstandard') in ["Standard", "NatDex"]
    ]

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)

def getSpecies():
    with open(OUTPUT_F_PATH) as f:
        return json.load(f)





