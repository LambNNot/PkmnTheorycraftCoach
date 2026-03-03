"""Contains helper functions surrounding Pokemon types"""
import json

def getAllMonoTypes() -> list[str]:
    """Generates a list of every single base Pokemon Type (excludes Stellar)"""
    pass

def getAllDualTypes() -> list[str]:
    """Generates a list of every single possible type combination in Pokemon"""
    pass

if __name__ == "__main__":

    with open('smogonData/typeData.json', 'r') as file: # Read in from typeData.json
        typeData:list[dict] = json.load(file)

    """
    typeData.json contains a list json object of many dictionaries, each representing an individual Pokemon Type
    Each dictionary contains:
        - name : The name of the type
        - atk_effectives : The attack multiplier of this type's attack against other types
        - genfamily : The Pokemon generations to which the type belong
        - description : A textual description of unique innate properties of the type
    """

    print([entry.get('name') for entry in typeData])
    pass

