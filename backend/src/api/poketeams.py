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
from src.api.pokesets import PokeSet


router = APIRouter(
    prefix="/pkteam",
    tags=["pkteam"],
    #dependencies=[Depends(auth.get_api_key)],
)

class PokeTeam(BaseModel):
    name: str
    author: str
    mons: List[PokeSet]

@router.post("/editTeam", status_code=status.HTTP_204_NO_CONTENT)
def editTeam(
    teamId: int,
    name: str,
    setIDs: List[int]
) -> None:
    setIDs = (setIDs + [None] * 6)[:6] # Validate setIDs

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                UPDATE poke_team
                SET
                    name = :name,
                    "set1ID" = :set1ID,
                    "set2ID" = :set2ID,
                    "set3ID" = :set3ID,
                    "set4ID" = :set4ID,
                    "set5ID" = :set5ID,
                    "set6ID" = :set6ID
                WHERE id = :teamId
                """
            ),
            {
                "teamId": teamId,
                "name": name,
                "set1ID": setIDs[0],
                "set2ID": setIDs[1],
                "set3ID": setIDs[2],
                "set4ID": setIDs[3],
                "set5ID": setIDs[4],
                "set6ID": setIDs[5],
            },
        )

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Team not found")

@router.post("/myteams", status_code=status.HTTP_201_CREATED)
def postUserteams(author: str) -> None:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO poke_team (
                    name,
                    "authorId",
                    "set1ID",
                    "set2ID",
                    "set3ID",
                    "set4ID",
                    "set5ID",
                    "set6ID"
                )
                SELECT
                    'New Team',
                    u.id,
                    NULL, NULL, NULL, NULL, NULL, NULL
                FROM "user" u
                WHERE u.username = :author
                """
            ),
            {"author": author},
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )


class GetTeamsArgs(BaseModel):
    user: str
@router.get("/myteams", response_model=List[PokeTeam])
def getUserTeams(
    user: Optional[str] = Query(None)
) -> List[PokeTeam]:
    if not user or user == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad user"
        )
    
    print(f"Fetching teams of user: {user}...")

    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    u.username as author, pt.*
                FROM poke_team pt
                LEFT JOIN "user" u
                    ON u.id = pt."authorId"
                WHERE u.username = :user
                """
            ),
            [{"user" : user}]
        ).all()
    
        teams: List[PokeTeam] = []
        for r in results:
            mons = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT ps.*, p.species, p.forme, p.dex_no as dex_no, i.name as item, a.name as ability, u.username as author
                    FROM pokeset ps
                    JOIN pokemon p
                        ON mon_id = p.id
                    JOIN item i
                        ON item_id = i.id
                    JOIN ability a
                        ON ability_id = a.id
                    JOIN "user" u
                        ON author_id = u.id
                    WHERE
                        ps.id in (:set1ID, :set2ID, :set3ID, :set4ID, :set5ID, :set6ID)
                    """
                ),
                [{
                    "set1ID" : r.set1ID or -1,
                    "set2ID" : r.set2ID or -1,
                    "set3ID" : r.set3ID or -1,
                    "set4ID" : r.set4ID or -1, 
                    "set5ID" : r.set5ID or -1,
                    "set6ID" : r.set6ID or -1,
                }]
            ).all()
            sets = [
                PokeSet(
                    name=s.name,
                    species=s.species,
                    forme=s.forme,
                    item=s.item,
                    ability=s.ability,
                    tera="Normal",
                    author=s.author,
                    dex_no=s.dex_no
                )
                for s in mons
            ]
            teams.append(
                PokeTeam(
                    name=r.name,
                    author=r.author,
                    mons = sets
                )
            )
        return teams






