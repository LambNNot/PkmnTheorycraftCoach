from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import APIRouter, Depends, status, Query, HTTPException
# import sqlalchemy.exc
from src.api import auth
import sqlalchemy
from src import database as db
# from typing import List, Self, Optional

# from datetime import date, datetime
# from psycopg import errors

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(auth.get_api_key)],
)


class UserPokesetCreate(BaseModel):
    user_id: int
    pokeset_id: int


class NewUserRequest(BaseModel):
    username: str
    password_hash: str
    is_public: bool = True
@router.post("/new", status_code=status.HTTP_201_CREATED)
def new_user(user: NewUserRequest) -> None:
    with db.engine.begin() as connection:
        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO "user" (username, password_hash, is_public)
                    VALUES (:username, :password_hash, :is_public)
                    """
                ),
                {
                    "username": user.username,
                    "password_hash": user.password_hash,
                    "is_public": user.is_public,
                },
            )
        except Exception as e:
            # Likely a uniqueness violation on username
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

@router.post("/new_user_pokeset", status_code=status.HTTP_201_CREATED)
def new_user_pokeset(body: UserPokesetCreate):
    """Relate a new pokeset and user"""
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO user_pokeset (user_id, pokeset_id)
                VALUES (:user_id, :pokeset_id)
                """
            ),
            {
                "user_id": body.user_id,
                "pokeset_id": body.pokeset_id,
            }
        )

@router.delete("/delete_user_pokeset", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_pokeset(body: UserPokesetCreate):
    """Remove relation between a pokeset and user"""
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM user_pokeset
                WHERE user_id = :user_id
                  AND pokeset_id = :pokeset_id
                """
            ),
            {
                "user_id": body.user_id,
                "pokeset_id": body.pokeset_id,
            }
        )

