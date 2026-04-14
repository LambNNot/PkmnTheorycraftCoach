import json
from pathlib import Path

CWD = Path(__file__).resolve().parent
ITEM_FILENAME = "itemData.json"
ITEM_F_PATH = CWD/ITEM_FILENAME

OUTPUT_FILENAME = "pkmn_items.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = ["name", "description"]

def getAllItems():
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    with open(ITEM_F_PATH) as f:
        itemData:list[dict] = json.load(f)

    print(len(itemData))
    print(list(itemData[0].keys()))

    parsed_results = [
        {
            v : a.get(v)
            for v in RELEVANT_FIELDS
        }
        for a in itemData
    ]

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)





