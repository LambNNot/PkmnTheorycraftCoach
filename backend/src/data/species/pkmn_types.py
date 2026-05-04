import json
from pathlib import Path
from typing import Tuple

CWD = Path(__file__).resolve().parent
TYPE_FILENAME = "typeData.json"
TYPE_F_PATH = CWD/TYPE_FILENAME

OUTPUT_FILENAME = "pkmn_types.json"
OUTPUT_F_PATH = CWD/OUTPUT_FILENAME

RELEVANT_FIELDS = ["name", "description"]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]

prime_idx_tracker = 0
def next_prime():
        global prime_idx_tracker
        curr = prime_idx_tracker
        prime_idx_tracker += 1
        return PRIMES[curr]


def getComponentTypes(typeCode: int) -> Tuple[str, str]:
    """
    Returns the constituent primes that make up a typecode in a 2-tuple.\n
    Ex. typeCode(6) = (2, 3)
    """
    for p in PRIMES:
        if typeCode % p == 0:
            return (p, typeCode / p)
    return -1


def create_weakness_table():

    raise NotImplementedError()

    output_file = "typeDataWithWeaknesses.json"
    output_path = CWD/output_file

    with open(TYPE_F_PATH) as f:
        typeData:list[dict] = json.load(f)

    # Init Weakness Table
    weakness_table:dict = {
        t.get("name") : []
        for t in typeData
    }

    pass # TODO

def getMonoTypeCode(type_: str) -> int:
    # Open file
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    # Load typecode table
    codeTable = {
        t.get("name").lower() : t.get("typeCode")
        for t in data
    }

    # Check for type
    if not (codeTable.get(type_.lower())):
        return -1

    # Return
    return codeTable.get(type_.lower())

def getDualTypeCode(t1: str, t2: str) -> int:
    """
    Every type is encoded as a unique prime number.
    Each dual type is encoded by the product of its two constituent types' prime encoding.
    """
    # Open file
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    # Load typecode table
    codeTable = {
        t.get("name").lower() : t.get("typeCode")
        for t in data
    }

    # Check for both types
    if not (codeTable.get(t1.lower()) and codeTable.get(t2.lower())):
        return -1

    # Return
    return codeTable.get(t1.lower()) * codeTable.get(t2.lower())

def getAllTypes() -> list:
    # Open file
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    # Load typecode table
    result:list = []
    codeTable:dict = {}
    for t in data:
        result.append(
            {
                "name" : t.get("name"),
                "typeCode" : t.get("typeCode"),
                "description" : t.get("description", "")
            }
        )
        codeTable.update(
            {t.get("typeCode") : t.get("name")}
        )
    
    first = 0
    second = first + 1
    limit = len(PRIMES)
    while (first < limit):
        if second == limit:
            first += 1
            second = first + 1
            continue
        result.append(
            {
                "typeCode" : PRIMES[first] * PRIMES[second],
                "name" : "-".join([codeTable.get(PRIMES[x]) for x in [first, second]]),
                "description" : ""
            }
        )
        second += 1
    return result

def getTypeDescription(t: str) -> str | None:
    # Open file
    with open(OUTPUT_F_PATH) as f:
        data = json.load(f)
    # Load typecode table
    codeTable = {
        d.get("name").lower() : d.get("description")
        for d in data
    }
    
    return codeTable.get(t)



if __name__ == "__main__":

    if (len(PRIMES) != 19):
        raise ValueError(f"Invalid num of primes for prime encoding: {len(PRIMES)}")

    with open(TYPE_F_PATH) as f:
        typeData:list[dict] = json.load(f)

    print(len(typeData))
    print(list(typeData[0].keys()))

    allTypes = [t.get("name") for t in typeData]
    if (len(allTypes) != 19) :
        raise ValueError(f"Invalid num of types: {len(allTypes)}")

    # Load monotypes
    parsed_results = [
        {
            "typeCode" : next_prime(),
            "name" : a.get("name").lower(),
            "atk_mus": [[mu[0].lower(), mu[1]] for mu in a.get("atk_effectives")],
            "description": a.get("description")


        }
        for a in typeData
    ]

    print(parsed_results)

    with open(OUTPUT_F_PATH, 'w') as f:
        json.dump(parsed_results, f, indent=4)

    print("-------------------------")
    print(getAllTypes())


def getTypeCode(type_one: str, type_two: str|None) -> int:
    """Utility function that fetches the corresponding typecode for querying"""
    isDualType = type_one is not None and type_two is not None
    if isDualType:
        return getDualTypeCode(type_one, type_two)
    elif type_one or type_two:
        return getMonoTypeCode(type_one if type_one else type_two)
    else:
        return 1 # Matches all types for type filter