import json
from pathlib import Path

CWD = Path(__file__).resolve().parent
SET_FILENAME = "setsData.json"
SET_F_PATH = CWD/SET_FILENAME

OUTPUT_FILENAME = "pkmn_sets.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = []

def getAllSets():
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    with open(SET_F_PATH) as f:
        setsData:list[dict] = json.load(f)

    print(len(setsData))
    print(list(setsData[0].keys()))

    parsed_results = []
    for a in setsData:
        evs = a.get("evconfigs", [{}])[0]
        ivs = a.get("ivconfigs", [{}])
        ivs = ivs[0] if len(ivs) > 0 else {}

        parsed = {
            "id": None,  # fill if you have it
            "name": a.get("name"),
            "species": a.get("pokemon"),
            "item": a.get("items", [None])[0],
            "ability": a.get("abilities", [None])[0],
            "nature": a.get("natures", [None])[0],

            "hp_ev": evs.get("hp", 0),
            "atk_ev": evs.get("atk", 0),
            "def_ev": evs.get("def", 0),
            "spa_ev": evs.get("spa", 0),
            "spd_ev": evs.get("spd", 0),
            "spe_ev": evs.get("spe", 0),

            "hp_iv": ivs.get("hp", 31),
            "atk_iv": ivs.get("atk", 31),
            "def_iv": ivs.get("def", 31),
            "spa_iv": ivs.get("spa", 31),
            "spd_iv": ivs.get("spd", 31),
            "spe_iv": ivs.get("spe", 31),

            "author_id": -1,  # Points to dummy user
        }

        parsed_results.append(parsed)

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)





