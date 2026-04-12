import json
from pathlib import Path

CWD = Path(__file__).resolve().parent
ABILITY_FILENAME = "abilityData.json"
ABILITY_F_PATH = CWD/ABILITY_FILENAME

OUTPUT_FILENAME = "pkmn_abilities.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = ["name", "description"]

def getAllAbilities():
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    with open(ABILITY_F_PATH) as f:
        abilityData:list[dict] = json.load(f)

    print(len(abilityData))
    print(list(abilityData[0].keys()))

    parsed_results = [
        {
            v : a.get(v)
            for v in RELEVANT_FIELDS
        }
        for a in abilityData
    ]

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)





