from pathlib import Path
from enum import Enum

from pydantic import BaseModel, Field


class BanTypes(Enum):
    permanent = "PERMANENT"
    under_review = "UNDER_REVIEW"


class ProviderTypes(Enum):
    battle_net = "battle"
    steam = "steam"
    uno = "uno"


class Cookies(BaseModel):
    file_path: Path | None = None
    value: dict[str, str]


class Account(BaseModel):
    username: str
    provider: ProviderTypes


class Profile(BaseModel):
    username: str
    email: str
    created: str
    accounts: list[Account]
    cookies: Cookies | None = None


class Ban(BaseModel):
    enforcement: BanTypes
    title: str
    can_appeal: bool = Field(alias="canAppeal")


class Status(BaseModel):
    success: str
    can_appeal: bool = Field(alias="canAppeal")
    bans: list[Ban]
    error: str
