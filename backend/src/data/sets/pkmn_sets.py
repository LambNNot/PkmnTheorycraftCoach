import json
from pathlib import Path

CWD = Path(__file__).resolve().parent
SET_FILENAME = "setsData.json"
SET_F_PATH = CWD/SET_FILENAME

OUTPUT_FILENAME = "pkmn_sets.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = []

def getAllItems():
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    with open(SET_F_PATH) as f:
        setsData:list[dict] = json.load(f)

    print(len(setsData))
    print(list(setsData[0].keys()))

    parsed_results = [
        {
            v : a.get(v)
            for v in RELEVANT_FIELDS
        }
        for a in setsData
    ]

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)





