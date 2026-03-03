from fastapi import APIRouter, Depends, status
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List, Optional
from pydantic import BaseModel
from src.data.species.pkmn_species import getSpecies

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

@router.post("/initSpecies", status_code=status.HTTP_204_NO_CONTENT)
def init_pkmn_species():

    BATCH_SIZE = 5000

    species_data = getSpecies()

    # Expecting a list[dict] already shaped like DB columns / named params
    rows = [r for r in species_data if isinstance(r, dict)]
    if not rows:
        return None

    def batched(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    with db.engine.begin() as connection:
        connection.execute(
                sqlalchemy.text(
                """
                DELETE FROM pokemon
                """
                )
            )
        for batch in batched(rows, BATCH_SIZE):
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO pokemon (
                        dex_no, species, type_code, forme,
                        ability_one_id, ability_two_id,
                        base_hp, base_atk, base_def, base_spa, base_spd, base_spe,
                        weight
                    )
                    VALUES (
                        :dex_no, :species, :typeCode, :forme,
                        :ability_one_id, :ability_two_id,
                        :base_hp, :base_atk, :base_def, :base_spa, :base_spd, :base_spe,
                        :weight
                    )
                    """
                ),
                batch
            )

    return None