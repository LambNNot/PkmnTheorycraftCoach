from bs4 import BeautifulSoup
import requests
import json
from time import sleep
from typing import List

RELEVANT_FORMATS = ["ZU", "PU", "NU", "RU", "UU", "OU", "Uber", "AG"]

def getAllStandardMons() -> List[str]:
    with open('src/main/resources/smogonData/pokemonData.json', 'r') as f:
        pkmn_data = json.load(f)

    return [pkmn.get('name') for pkmn in pkmn_data if pkmn.get('isNonstandard') == "Standard"]

def getStrats(pokemon: str) -> List[dict]:
    """
    Scrape documented strategies of a given pokemon from Smogon for relevant formats.
    Strategy written descriptions are modified to be blank for data processing.
    Formats are appended to strategies for classification.
    """
    print(f"Fetching strats for {pokemon}...")
    response = requests.get(f"https://www.smogon.com/dex/sv/pokemon/{pokemon.lower()}/")
    if (response.status_code != 200):
        raise RuntimeError("Scraping failed")

    soup = BeautifulSoup(response.content, 'html.parser')

    dex_script = soup.find('script', type='text/javascript')
    script_text:str = dex_script.text

    json_start = script_text.find("{")
    parsed_dex_settings:dict = json.loads(script_text[json_start:])
    pkmn_dump:dict = parsed_dex_settings.get('injectRpcs')[2][1]
    strategies:list = pkmn_dump.get('strategies')

    results = []

    for strat in strategies:
        strat:dict
        if strat.get('format') in RELEVANT_FORMATS:
            for set in strat.get('movesets'):
                set:dict
                set.update({'description' : ''})
                set.update({'format' : strat.get('format')})
                results.append(set)
                # print(f"\n-----\nFormat: {strat.get('format')}\n{set}")

    return results

if __name__ == "__main__":
    
    # Load all saved Standard Pokemon
    standardMons = getAllStandardMons()
    count = len(standardMons)
    # print(standardMons)

    # Note: We are NOT cleaning duplicates as of the moment.
    #       Different forms may contribute multiple times to the dataset.

    sets = []
    counter = 0
    for mon in standardMons:
        print(f"{count - counter}: ", end="")
        sets.extend(getStrats(mon))
        counter += 1

    with open('src/main/resources/smogonData/sets.json', 'w') as f:
        f.write(json.dumps(sets, indent=2))
    
    # # Actual Scraping Logic
    # print(getStrats("Ogerpon-Hearthflame-Tera"))
    # print(getStrats("Ogerpon-Hearthflame"))


