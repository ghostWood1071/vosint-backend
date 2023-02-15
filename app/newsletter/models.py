from enum import Enum
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Tags(str, Enum):
    newsletter = "newsletter"  # Giỏ tin
    field = "field"  # Lĩnh vực tin
    topic = "topic"  # Danh mục chủ đề


class NewsLetterModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    user_id: str = Field(default_factory=ObjectId)
    parent_id: str = Field(default_factory=ObjectId)
    title: str
    tags: Tags = Tags.newsletter
    news_id: list[str]


class NewsLetterCreateModel(BaseModel):
    parent_id: str | None
    title: str
    tags: Tags


class NewsLetterUpdateModel(BaseModel):
    parent_id: str | None
    title: str | None
    tags: Optional[Tags]
