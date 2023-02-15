from enum import Enum
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Tags(str, Enum):
    newsletter = "newsletter"
    field = "field"
    topic = "topic"


class NewsLetterModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    user_id: str = Field(default_factory=ObjectId)
    parent_id: str = Field(default_factory=ObjectId)
    title: str
    tags: list[Tags] = [Tags.newsletter]


class NewsLetterCreateModel(BaseModel):
    parent_id: str | None
    title: str
    tags: list[Tags] | None


class NewsLetterUpdateModel(BaseModel):
    parent_id: str | None
    title: str | None
    tags: list[Tags] | None
