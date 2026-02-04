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
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{species_name}", response_model=Pokemon)
def get_pokemon(species_name):
    """Retrieves a pokemon based on species name."""
    with db.engine.begin() as connection:
        pass
    return Pokemon(
        dex_no=303,
        species="Mawile",
        typeCode=0,
        forme="Mega",
        ability_one_id=0,
        ability_two_id=0,
        base_hp=50,
        base_atk=105,
        base_def=125,
        base_spa=55,
        base_spd=95,
        base_spe=50,
        weight=23.5
    )