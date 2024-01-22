from enum import Enum
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

class NewsletterTag(str, Enum):
    SELFS = "selfs"
    ARCHIVE = "archives"


class NewsLetterModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    user_id: str = Field(default_factory=ObjectId)
    parent_id: str = Field(default_factory=ObjectId)
    title: str
    tag: NewsletterTag = NewsletterTag.ARCHIVE
    news_id: List[str]
    required_keyword: List[str]
    exclusion_keyword: str


class NewsSampleModel(BaseModel):
    id: str
    title: str
    content: str
    link: Optional[str]


class NewsSampleModel(BaseModel):
    id: str
    title: str
    content: str
    link: Optional[str]


class NewsLetterCreateModel(BaseModel):
    parent_id: str | None
    title: str
    tag: NewsletterTag
    required_keyword: Optional[list[str]]
    exclusion_keyword: Optional[str]
    keyword_vi: Optional[object]
    keyword_en: Optional[object]
    keyword_cn: Optional[object]
    keyword_ru: Optional[object]
    is_sample: Optional[bool]
    news_samples: Optional[list[NewsSampleModel]]


class NewsLetterUpdateModel(BaseModel):
    parent_id: str | None
    title: str | None
    tag: Optional[NewsletterTag]
    required_keyword: Optional[list[str]]
    exclusion_keyword: Optional[str]
    keyword_vi: Optional[object]
    keyword_en: Optional[object]
    keyword_cn: Optional[object]
    keyword_ru: Optional[object]
    is_sample: Optional[bool]
    news_samples: Optional[list[NewsSampleModel]]


class NewsletterDeleteMany(BaseModel):
    newsletter_ids: List[str]
