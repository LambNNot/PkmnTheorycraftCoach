from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import APIRouter, Depends, status, Query, HTTPException
import sqlalchemy.exc
from src.api import auth
import sqlalchemy
from src import database as db
from typing import List, Self, Optional
from datetime import date, datetime
from psycopg import errors
from src.db.schemas.schemas import Pokemon

router = APIRouter(
    prefix="/pkmn",
    tags=["pkmn"],
    #dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{species_name}", response_model=List[Pokemon])
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
            for result in results
        ]
    
@router.get("/", response_model=List[Pokemon])
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
            Pokemon(
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
