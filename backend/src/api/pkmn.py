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
from src.data.species.pkmn_types import getDualTypeCode, getMonoTypeCode

router = APIRouter(
    prefix="/pkmn",
    tags=["pkmn"],
    #dependencies=[Depends(auth.get_api_key)],
)

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
            PokemonSchema(
                dex_no=result.dex_no,
                species=result.species,
                typeCode=result.type_code,
                forme=result.forme,
                ability_one_id=result.ability_one_id,
                ability_two_id=result.ability_two_id,
                ability_hidden_id=result.ability_hidden_id,
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
    
class NewPokemon(BaseModel):
    dex_no: int
    species: str
    type_one: str
    type_two: str | None
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
def post_species(species_data: NewPokemon) -> None:
    # Get typecode
    if (not species_data.type_two == ""):
        typeCode = getDualTypeCode(species_data.type_one, species_data.type_two)
    else:
        typeCode = getMonoTypeCode(species_data.type_one)

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
    
@router.post("/search", response_model=List[PokemonSchema])
def search_species(
    species_name: Optional[str] = Query(None),
    ability: Optional[str] = Query(None),
    type_one: Optional[str] = Query(None),
    type_two: Optional[str] = Query(None),
    forme: Optional[str] = Query(None),
) -> List[PokemonSchema]:
    print("Received search query:")
    print(f"species_name: {species_name}")
    print(f"ability: {ability}")
    print(f"type_one: {type_one}")
    print(f"type_two: {type_two}")
    print(f"forme: {forme}")

    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    dex_no, species, type_code, forme,
                    ability_one_id, ability_two_id, ability_hidden_id,
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
                WHERE species ILIKE '%' || COALESCE(:species_name, '') || '%'
                    AND forme ILIKE '%' || COALESCE(:forme, '') || '%'
                    AND (
                        a1.name ILIKE '%' || COALESCE(:ability, '') || '%'
                        OR a2.name ILIKE '%' || COALESCE(:ability, '') || '%'
                        OR ah.name ILIKE '%' || COALESCE(:ability, '') || '%'
                    )
                ORDER BY
                    dex_no ASC
                LIMIT 10
                """
            ),
            [{
                "species_name" : species_name,
                "forme": forme,
                "ability": ability
            }]
        ).all()
        
        return [
            PokemonSchema(
                dex_no=result.dex_no,
                species=result.species,
                typeCode=result.type_code,
                forme=result.forme,
                ability_one_id=result.ability_one_id,
                ability_two_id=result.ability_two_id,
                ability_hidden_id=result.ability_hidden_id,
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