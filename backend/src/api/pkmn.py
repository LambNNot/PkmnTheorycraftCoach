from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import APIRouter, Depends, status, Query, HTTPException
import sqlalchemy.exc
from src.api import auth
import sqlalchemy
from src import database as db
from typing import List, Self, Optional
from datetime import date, datetime
from psycopg import errors
from src.db.schemas.schemas import PokemonSchema
from src.data.species.pkmn_types import getTypeCode, getComponentTypes

router = APIRouter(
    prefix="/pkmn",
    tags=["pkmn"],
    #dependencies=[Depends(auth.get_api_key)],
)
    
@router.get("/", response_model=List[PokemonSchema])
def get_pokemon():
    """Retrieves a pokemon based on species name."""
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM pokemon
                ORDER BY dex_no ASC
                """
            )
        ).all()

        return [
            PokemonSchema(
                dex_no=result.dex_no,
                species=result.species,
                typeCode=result.type_code,
                forme=result.forme,
                ability_one_id=result.ability_one_id,
                ability_two_id=result.ability_two_id,
                base_hp=result.base_hp,
                base_atk=result.base_atk,
                base_def=result.base_def,
                base_spa=result.base_spa,
                base_spd=result.base_spd,
                base_spe=result.base_spe,
                weight=result.weight,
            )
            for result in rows
        ]
    
class Pokemon(BaseModel):
    dex_no: int
    species: str
    type: str | None
    forme: str
    ability_one: str
    ability_two: str | None
    ability_hidden: str | None
    base_hp: int
    base_atk: int
    base_def: int
    base_spa: int
    base_spd: int
    base_spe: int
    weight: float

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_species(species_data: Pokemon) -> None:
    # Get typecode
    typeCode = getTypeCode(species_data.type_one, species_data.type_two if not species_data.type_two == "" else None)

    raise NotImplementedError()
    with db.engine.begin() as connection:

        ability_names = [
                species_data.ability_one,
                species_data.ability_two,
                species_data.ability_hidden
        ]

        # Get ability ids
        ability_ids = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM ability
                WHERE name = :name
                """
            ),
            []
        ) # TODO
        
        # Insert
        pass
    
@router.get("/search_species", response_model=List[Pokemon])
def search_species(
    species_name: Optional[str] = Query(None),
    ability: Optional[str] = Query(None),
    type_one: Optional[str] = Query(None),
    type_two: Optional[str] = Query(None),
    forme: Optional[str] = Query(None),
) -> List[Pokemon]:
    query = {
        "species_name": species_name,
        "ability": ability,
        "type_one": type_one,
        "type_two": type_two,
        "forme": forme,
    }
    print("Received search query:")
    for k in query.keys():
        if query[k]: print(f"{k}: {query[k]}")

    typeCode = getTypeCode(type_one, type_two)
    if typeCode == -1: raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid type(s)")

    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    dex_no, species, t.name as type, forme,
                    a1.name as ability_one, a2.name as ability_two, ah.name as ability_hidden,
                    base_hp, base_atk, base_def,
                    base_spa, base_spd, base_spe,
                    weight
                FROM pokemon
                JOIN ability a1
                    ON a1.id = ability_one_id
                LEFT JOIN ability a2
                    ON a2.id = ability_two_id
                LEFT JOIN ability ah
                    ON ah.id = ability_hidden_id
                JOIN type t
                    ON t.type_code = pokemon.type_code
                WHERE species ILIKE '%' || COALESCE(:species_name, '') || '%'
                    AND forme ILIKE '%' || COALESCE(:forme, '') || '%'
                    AND (
                        a1.name ILIKE '%' || COALESCE(:ability, '') || '%'
                        OR a2.name ILIKE '%' || COALESCE(:ability, '') || '%'
                        OR ah.name ILIKE '%' || COALESCE(:ability, '') || '%'
                    )
                    AND pokemon.type_code % :typeCode = 0
                ORDER BY
                    dex_no ASC
                LIMIT 100
                """
            ),
            [{
                "species_name" : species_name,
                "forme": forme,
                "ability": ability,
                "typeCode": typeCode
            }]
        ).all()
        
        return [
            Pokemon(
                dex_no=result.dex_no,
                species=result.species,
                type=result.type,
                forme=result.forme,
                ability_one=result.ability_one,
                ability_two=result.ability_two,
                ability_hidden=result.ability_hidden,
                base_hp=result.base_hp,
                base_atk=result.base_atk,
                base_def=result.base_def,
                base_spa=result.base_spa,
                base_spd=result.base_spd,
                base_spe=result.base_spe,
                weight=result.weight,
            )
            for result in results
        ]


@router.get("/{species_name}", response_model=List[PokemonSchema])
def get_pokemon(species_name):
    """Retrieves a pokemon based on species name."""
    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM pokemon
                WHERE species ILIKE '%' || :species_name  || '%'
                ORDER BY dex_no ASC
                """
            ),
            [{"species_name" : species_name}]
        ).all()

        if results is None:
            return []

        return [
            Pokemon(
                dex_no=result.dex_no,
                species=result.species,
                type=result.type,
                forme=result.forme,
                ability_one=result.ability_one,
                ability_two=result.ability_two,
                ability_hidden=result.ability_hidden,
                base_hp=result.base_hp,
                base_atk=result.base_atk,
                base_def=result.base_def,
                base_spa=result.base_spa,
                base_spd=result.base_spd,
                base_spe=result.base_spe,
                weight=result.weight,
            )
            for result in results
        ]
    
class UserCreate(BaseModel):
    username: str
    password: str
    is_public: bool

    
@router.post("/new_user", status_code=status.HTTP_201_CREATED)
def new_user(body: UserCreate):
    """Create a new user"""

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO "user" (username, password_hash, is_public)
                VALUES (:username, :password_hash, :is_public)
                """
            ),
            {
                "username": body.username,
                "password_hash": body.password,
                "is_public": body.is_public,
            }
        )