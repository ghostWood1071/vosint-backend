from enum import Enum
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Tag(str, Enum):
    gio_tin = "gio_tin"
    linh_vuc = "linh_vuc"
    chu_de = "chu_de"


class NewsLetterModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    user_id: str = Field(default_factory=ObjectId)
    parent_id: str = Field(default_factory=ObjectId)
    title: str
    tag: Tag = Tag.gio_tin
    news_id: list[str]


class NewsLetterCreateModel(BaseModel):
    parent_id: str | None
    title: str
    tag: Tag
    required_keyword: Optional[list[str]]
    exclusion_keyword: Optional[str]


class NewsLetterUpdateModel(BaseModel):
    parent_id: str | None
    title: str | None
    tag: Optional[Tag]
    required_keyword: Optional[list[str]]
    exclusion_keyword: Optional[str]
