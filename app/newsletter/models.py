from enum import Enum
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Tags(str, Enum):
    newsletters = "newsletters"
    fields = "fields"
    topic = "topic"


class NewsLetterModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    user_id: str = Field(default_factory=ObjectId)
    parent_id: str = Field(default_factory=ObjectId)
    title: str
    tags: list[Tags] = [Tags.newsletters]


class NewsLetterCreateModel(BaseModel):
    user_id: str
    parent_id: str | None
    title: str
    tags: list[Tags] | None


class NewsLetterUpdateModel(BaseModel):
    parent_id: str | None = Field(default_factory=ObjectId)
    title: str | None
    tags: list[Tags] | None
