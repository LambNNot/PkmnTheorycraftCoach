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


router = APIRouter(
    prefix="/pkset",
    tags=["pkset"],
    #dependencies=[Depends(auth.get_api_key)],
)

class PokeSet(BaseModel):
    name: str
    species: str
    forme: str
    item: str
    ability: str
    tera: str
    author: str
    dex_no: int


@router.get("/search_set", response_model=List[PokeSet])
def search_set(
    set_name: Optional[str] = Query(None),
    species_name: Optional[str] = Query(None),
    item: Optional[str] = Query(None),
    ability: Optional[str] = Query(None),
    type_one: Optional[str] = Query(None),
    type_two: Optional[str] = Query(None),
    forme: Optional[str] = Query(None),
    author: Optional[str] = Query(None)
) -> List[PokeSet]:
    print("Received search query:")
    query = {
        "set_name": set_name,
        "species_name": species_name,
        "item": item,
        "ability": ability,
        "type_one": type_one,
        "type_two": type_two,
        "forme": forme,
        "author": author,
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
                    pokeset.name as name, p.species as species, i.name as item, a.name as ability, t.name as type, p.forme as forme, u.username as author, p.dex_no as dex_no
                FROM pokeset
                JOIN pokemon p
                    ON mon_id = p.id
                JOIN item i
                    ON item_id = i.id
                JOIN ability a
                    ON ability_id = a.id
                JOIN type t
                    ON t.type_code = p.type_code
                JOIN "user" u
                    ON author_id = u.id
                LEFT JOIN user_pokeset ups
                    ON user_id = u.id
                WHERE pokeset.name ILIKE '%' || COALESCE(:set_name, '') || '%'
                    AND p.species ILIKE '%' || COALESCE(:species_name, '') || '%'
                    AND i.name ILIKE '%' || COALESCE(:item, '') || '%'
                    AND p.forme ILIKE '%' || COALESCE(:forme, '') || '%'
                    AND a.name ILIKE '%' || COALESCE(:ability, '') || '%'
                    AND t.type_code % :typeCode = 0
                    AND (
                        u.username ILIKE '%' || COALESCE(:author, '') || '%'
                    )
                ORDER BY
                    dex_no ASC
                LIMIT 100
                """
            ),
            [{
                "set_name": set_name,
                "species_name" : species_name,
                "item": item,
                "ability": ability,
                "forme": forme,
                "typeCode": typeCode,
                "author": author,
            }]
        ).all()
        
    return [
        PokeSet(
            name=result.name,
            species=result.species,
            forme=result.forme,
            item=result.item,
            ability=result.ability,
            tera="Normal",
            author=result.author,
            dex_no=result.dex_no
        )
        for result in results
    ]