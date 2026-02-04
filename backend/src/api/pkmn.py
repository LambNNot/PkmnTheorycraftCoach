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