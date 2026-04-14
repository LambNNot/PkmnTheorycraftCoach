from fastapi import APIRouter, Depends, status
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List, Optional
from pydantic import BaseModel
from src.data.species.pkmn_species import getSpecies, getAllSpecies
from src.data.species.pkmn_types import getAllTypes
from src.data.abilities.pkmn_abilities import getAllAbilities
from src.data.items.pkmn_items import getAllItems
from src.data.natures.pkmn_natures import getAllNatures
from src.data.sets.pkmn_sets import getAllSets


PKMN_SPECIES_PATH = "../data/species/pkmn_species.json"

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[
        #Depends(auth.get_api_key)
    ],
)


class AutoWarnResponse(BaseModel):
    affected_users: List[str]


@router.post("/autowarn", response_model=AutoWarnResponse)
def do_autowarn(tolerance: int = 5, user_id: Optional[int] = None):
    """
    Automatically set the status of user(s) with a specific number of recent reports to 'probation'
    """
    with db.engine.begin() as connection:
        if not user_id:
            query = """
                WITH affected_users as (
                    SELECT 
                        user_id
                    FROM reports
                    WHERE
                        ((now()::date - date_reported::date) / 7) < 2
                        AND status IN ('Pending', 'Reviewed')
                    GROUP BY user_id
                    HAVING COUNT(*) >= :tolerance
                )
                UPDATE users
                SET
                    status = 'probation'
                FROM affected_users as au
                WHERE users.id = au.user_id
                RETURNING users.username
            """
            params = {"tolerance": tolerance}
        else:
            query = """
                UPDATE users
                SET status = 'probation'
                WHERE id = :UId AND (
                    SELECT COUNT(*)
                    FROM reports
                    WHERE 
                        user_id = :UId
                        AND ((now()::date - date_reported::date) / 7) < 2
                        AND status IN ('Pending', 'Reviewed')
                ) >= :tolerance
                RETURNING username
            """
            params = {"UId": user_id, "tolerance": tolerance}

        users = connection.execute(sqlalchemy.text(query), params).all()

        return AutoWarnResponse(affected_users=[user.username for user in users])

@router.delete("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_data():
    """
    Truncate all data from all tables; start fresh.
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                TRUNCATE
                    games,
                    reports,
                    showcase_comments,
                    showcase_views,
                    showcases,
                    users
                RESTART IDENTITY
                CASCADE
                """
            )
        )

@router.post("/initTypes", status_code=status.HTTP_200_OK)
def init_pkmn_types():
    print("Retrieving all types...", sep=" ")
    allTypes = getAllTypes()
    print("SUCCESS")

    print("Upserting all types...", sep=" ")
    with db.engine.begin() as connection:
        connection.execute( 
            sqlalchemy.text(
                """
                INSERT INTO type (
                    type_code, name, description
                )
                VALUES (
                    :typeCode, :name, :description
                )
                ON CONFLICT (type_code)
                DO UPDATE SET
                    name        = EXCLUDED.name,
                    description = EXCLUDED.description
                """
            ),
            [
                {field : t.get(field) for field in ["typeCode", "name", "description"]}
                for t in allTypes
            ]
        )
    print("SUCCESS")
    return status.HTTP_200_OK

@router.post("/initAbilities", status_code=status.HTTP_200_OK)
def init_pkmn_abilities():
    print("Retrieving all abilities...", sep=" ")
    allAbilities = getAllAbilities()
    print("SUCCESS")

    print("Upserting abilities...", sep=" ")
    with db.engine.begin() as connection:
        connection.execute( 
            sqlalchemy.text(
                """
                INSERT INTO ability (
                    name, description
                )
                VALUES (
                    :name, :description
                )
                ON CONFLICT (name)
                DO UPDATE SET
                    description = EXCLUDED.description
                """
            ),
            [
                {field : t.get(field) for field in ["name", "description"]}
                for t in allAbilities
            ]
        )
    print("SUCCESS")
    return status.HTTP_200_OK


@router.post("/initItems", status_code=status.HTTP_200_OK)
def init_pkmn_items():
    print("Retrieving all items...", sep=" ")
    allItems = getAllItems()
    print("SUCCESS")

    print("Upserting items...", sep=" ")
    with db.engine.begin() as connection:
        connection.execute( 
            sqlalchemy.text(
                """
                INSERT INTO item (
                    name, description
                )
                VALUES (
                    :name, :description
                )
                ON CONFLICT (name)
                DO UPDATE SET
                    description = EXCLUDED.description
                """
            ),
            [
                {field : t.get(field) for field in ["name", "description"]}
                for t in allItems
            ]
        )
    print("SUCCESS")
    return status.HTTP_200_OK


@router.post("/initNatures", status_code=status.HTTP_200_OK)
def init_pkmn_natures():
    print("Retrieving all natures...", sep=" ")
    allNatures = getAllNatures()
    print("SUCCESS")

    print("Upserting natures...", sep=" ")
    with db.engine.begin() as connection:
        connection.execute( 
            sqlalchemy.text(
                """
                INSERT INTO nature (
                    name, hp, atk, dfn, spa, spd, spe, summary
                )
                VALUES (
                    :name, :hp, :atk, :dfn, :spa, :spd, :spe, :summary
                )
                ON CONFLICT (name)
                DO UPDATE SET
                    hp = EXCLUDED.hp,
                    atk = EXCLUDED.atk,
                    dfn = EXCLUDED.dfn,
                    spa = EXCLUDED.spa,
                    spd = EXCLUDED.spd,
                    spe = EXCLUDED.spe,
                    summary = EXCLUDED.summary
                """
            ),
            [
                {
                    field : t.get(field)
                    for field in ["name", "hp", "atk", "dfn", "spa", "spd", "spe", "summary"]
                }
                for t in allNatures
            ]
        )
    print("SUCCESS")
    return status.HTTP_200_OK

@router.post("/initSpecies", status_code=status.HTTP_200_OK)
def init_pkmn_species():
    print("Retrieving all species...", sep = "")
    allSpecies = getAllSpecies()
    print("SUCCESS")

    print("Upserting all species...")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                WITH input AS (
                SELECT
                    :dex_no  AS dex_no,
                    :species AS species,
                    :typeCode  AS type_code,
                    :forme AS forme,
                    :ability_one AS ability_one_name,
                    :ability_two AS ability_two_name,
                    :ability_hidden AS ability_hidden_name,
                    :base_hp  AS base_hp,
                    :base_atk  AS base_atk,
                    :base_def AS base_def,
                    :base_spa AS base_spa,
                    :base_spd AS base_spd,
                    :base_spe AS base_spe,
                    :weight AS weight
                )
                INSERT INTO pokemon (
                    dex_no, species, type_code, forme,
                    ability_one_id, ability_two_id, ability_hidden_id,
                    base_hp, base_atk, base_def, base_spa, base_spd, base_spe, weight
                )
                SELECT
                    i.dex_no, i.species, i.type_code, i.forme,
                    a1.id,
                    a2.id,
                    ah.id,
                    i.base_hp, i.base_atk, i.base_def, i.base_spa, i.base_spd, i.base_spe, i.weight
                FROM input i
                JOIN ability a1
                    ON a1.name = i.ability_one_name
                LEFT JOIN ability a2
                    ON a2.name = i.ability_two_name
                LEFT JOIN ability ah
                    ON ah.name = i.ability_hidden_name;
                """
            ),
            [
                {
                    field : s.get(field)
                    for field in [
                        "dex_no", "species", "typeCode", "forme",
                        "ability_one", "ability_two", "ability_hidden",
                        "base_hp", "base_atk", "base_def",
                        "base_spa", "base_spd", "base_spe", "weight"
                    ]
                }
                for s in allSpecies
            ]
        )
    print("SUCCESS")

@router.post("/initSets", status_code=status.HTTP_200_OK)
def init_pkmn_sets():
    print("Retrieving all sets...", sep = "")
    allSets = getAllSets()
    print("SUCCESS")

    print("Upserting all sets...")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                WITH input AS (
                    SELECT
                        :id AS id,
                        :name AS name,

                        :species AS species,
                        :item AS item,
                        :ability AS ability,
                        :nature AS nature,

                        :hp_ev AS hp_ev,
                        :atk_ev AS atk_ev,
                        :def_ev AS def_ev,
                        :spa_ev AS spa_ev,
                        :spd_ev AS spd_ev,
                        :spe_ev AS spe_ev,

                        :hp_iv AS hp_iv,
                        :atk_iv AS atk_iv,
                        :def_iv AS def_iv,
                        :spa_iv AS spa_iv,
                        :spd_iv AS spd_iv,
                        :spe_iv AS spe_iv
                )
                INSERT INTO pokeset (
                    name,

                    mon_id,
                    item_id,
                    ability_id,
                    nature_id,

                    hp_ev,
                    atk_ev,
                    def_ev,
                    spa_ev,
                    spd_ev,
                    spe_ev,

                    hp_iv,
                    atk_iv,
                    def_iv,
                    spa_iv,
                    spd_iv,
                    spe_iv,

                    author_id
                )
                SELECT
                    i.name, p.id, item.id, a.id, n.id,
                    i.hp_ev, i.atk_ev, i.def_ev, spa_ev, spd_ev, spe_ev,
                    hp_iv, atk_iv, def_iv, spa_iv, spd_iv, spe_iv, -1
                FROM input i
                JOIN pokemon p
                    ON i.species = p.species
                JOIN item 
                    ON i.item = item.name
                JOIN ability a
                    ON i.ability = a.name
                JOIN nature n
                    ON i.nature = n.name
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,

                    mon_id = EXCLUDED.mon_id,
                    item_id = EXCLUDED.item_id,
                    ability_id = EXCLUDED.ability_id,
                    nature_id = EXCLUDED.nature_id,

                    hp_ev = EXCLUDED.hp_ev,
                    atk_ev = EXCLUDED.atk_ev,
                    def_ev = EXCLUDED.def_ev,
                    spa_ev = EXCLUDED.spa_ev,
                    spd_ev = EXCLUDED.spd_ev,
                    spe_ev = EXCLUDED.spe_ev,

                    hp_iv = EXCLUDED.hp_iv,
                    atk_iv = EXCLUDED.atk_iv,
                    def_iv = EXCLUDED.def_iv,
                    spa_iv = EXCLUDED.spa_iv,
                    spd_iv = EXCLUDED.spd_iv,
                    spe_iv = EXCLUDED.spe_iv
                """
            ),
            [
                {
                    "id": s["id"],
                    "name": s["name"],

                    "species": s["species"],
                    "item": s["item"],
                    "ability": s["ability"],
                    "nature": s["nature"],

                    "hp_ev": s["hp_ev"],
                    "atk_ev": s["atk_ev"],
                    "def_ev": s["def_ev"],
                    "spa_ev": s["spa_ev"],
                    "spd_ev": s["spd_ev"],
                    "spe_ev": s["spe_ev"],

                    "hp_iv": s["hp_iv"],
                    "atk_iv": s["atk_iv"],
                    "def_iv": s["def_iv"],
                    "spa_iv": s["spa_iv"],
                    "spd_iv": s["spd_iv"],
                    "spe_iv": s["spe_iv"],
                }
                for s in allSets
            ]
        )

    print("SUCCESS")


@router.delete("/pkmn", status_code=status.HTTP_200_OK)
def del_pkmn():
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("TRUNCATE TABLE item, nature, pokemon, pokeset, type_effectiveness, type")
        )
    
    return status.HTTP_200_OK