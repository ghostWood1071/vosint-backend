from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Status(str, Enum):
    enable = "enable"
    disable = "disable"


class Keyword(BaseModel):
    vi: str = Field(...)
    en: str = Field(...)
    ru: str = Field(...)
    cn: str = Field(...)


class CreateOrganize(BaseModel):
    organize_name: str = Field(...)
    facebook_link: str = Field(...)
    twitter_link: str = Field(...)
    profile_link: str = Field(...)
    avatar_url: str = Field(...)
    profile: str = Field(...)
    keywords: Keyword
    status: Status

    class config:
        orm_mode = True


class UpdateOrganize(BaseModel):
    organize_name: Optional[str]
    facebook_link: Optional[str]
    twitter_link: Optional[str]
    profile_link: Optional[str]
    avatar_url: Optional[str]
    profile: Optional[str]
    keywords: Keyword
    status: Optional[str]

    class config:
        orm_mode = True
