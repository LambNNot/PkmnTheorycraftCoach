from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Self, List
from datetime import date, datetime


class Color(str, Enum):
    black = "black"
    white = "white"


class TimeControl(str, Enum):
    classical = "classical"
    rapid = "rapid"
    blitz = "blitz"
    bullet = "bullet"


class GameStatus(str, Enum):
    win = "win"
    loss = "loss"
    draw = "draw"


class GameModel(BaseModel):
    game_id: int
    black: int
    white: int
    winner: Color | None
    time_control: TimeControl
    duration_in_ms: int = Field(
        ge=0, description="Time must be non-zero and non-negative"
    )
    date_played: datetime

    @model_validator(mode="after")
    def validate_color(self) -> Self:
        if self.black == self.white:
            raise ValueError("the same player can't be both black and white'")
        return self


class Showcase(BaseModel):
    showcase_id: int
    created_by: str
    title: str
    views: int
    likes: int
    caption: str
    date_created: date
    game_id: int

class PokemonSchema(BaseModel):
    dex_no: int
    species: str
    typeCode: int
    forme: str
    ability_one_id: int
    ability_two_id: int | None
    ability_hidden_id: int | None
    base_hp: int
    base_atk: int
    base_def: int
    base_spa: int
    base_spd: int
    base_spe: int
    weight: float

class AbilitySchema(BaseModel):
    id: int
    name: str
    description: str

class ItemSchema(BaseModel):
    id: int
    name: str
    description: str

class TypeSchema(BaseModel):
    id: int
    typeCode: int
    name: str
    description: str

class TypeEffectivenessSchema(BaseModel):
    attack_type_id: int
    defense_type_id: int
    multiplier: float

class NatureSchema(BaseModel):
    id: int
    name: str
    hp: float
    atk: float
    dfn: float
    spa: float
    spd: float
    spe: float
    summary: str


class PokeSetSchema(BaseModel): # Moves not yet implemented
    id: int
    name: str
    mon_id: int
    item_id: int | None
    ability_id: int
    nature_id: int
    hp_ev: int
    atk_ev: int
    def_ev: int
    spa_ev: int
    spd_ev: int
    spe_ev: int
    hp_iv: int
    atk_iv: int
    def_iv: int
    spa_iv: int
    spd_iv: int
    spe_iv: int
    author_id: int

class User(BaseModel):
    id: int
    username: str
    password_hash: str
    is_public: bool

class PokeTeamsSchema(BaseModel):
    id: int                 # Auto-incrementing primary key
    name: str
    authorId: int           # Foreign Key to User Table
    set1ID: int | None      # 1-6 Foreign keys to PokeSet table
    set2ID: int | None
    set3ID: int | None
    set4ID: int | None
    set5ID: int | None
    set6ID: int | None

    



    