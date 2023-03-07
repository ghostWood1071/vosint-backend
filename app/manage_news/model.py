import re
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class CreateSourceGroup(BaseModel):
    user_id: str
    source_name: str
    news: list[str] = []
    is_hide: bool = False
    class config:
        orm_mode = True

class CreateSource(BaseModel):
    id_source: str
    name: str
    # host_name: Optional[str]
    # language: Optional[str]
    publishing_country: str
    is_hide: bool = False
    # source_type: Optional[str]

class UpdateSourceGroup(BaseModel):
    source_name: Optional[str]
    news: list[str] = []
    is_hide: Optional[bool]
    class config:
        orm_mode = True

class UpdateState(BaseModel):
    
    class config:
        orm_mode = True
