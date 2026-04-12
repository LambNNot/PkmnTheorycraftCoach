import json
from pathlib import Path

CWD = Path(__file__).resolve().parent
NATURE_FILENAME = "natureData.json"
NATURE_F_PATH = CWD/NATURE_FILENAME

OUTPUT_FILENAME = "pkmn_natures.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = ["name", "hp", "atk", "def", "spa", "spd", "spe", "summary"]

def getAllNatures():
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    return [
        {
            "name": n.get("name"),
            "hp": n.get("hp"),
            "atk": n.get("atk"),
            "dfn": n.get("def"),
            "spa": n.get("spa"),
            "spd": n.get("spd"),
            "spe": n.get("spe"),
            "summary": n.get("summary"),
        }
        for n in data
    ]

if __name__ == "__main__":

    with open(NATURE_F_PATH) as f:
        natureData:list[dict] = json.load(f)

    print(len(natureData))
    print(list(natureData[0].keys()))

    parsed_results = [
        {
            v : a.get(v)
            for v in RELEVANT_FIELDS
        }
        for a in natureData
    ]

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)





