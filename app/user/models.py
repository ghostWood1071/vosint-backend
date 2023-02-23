from enum import Enum
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = "admin"
    expert = "expert"
    leader = "leader"


class UserCreateModel(BaseModel):
    username: str
    password: str
    full_name: str
    role: Role
    vital_list: Optional[list[str]]


class UserUpdateModel(BaseModel):
    username: str
    password: str
    full_name: str


class UserLoginModel(BaseModel):
    username: str
    password: str

class VitalModel(BaseModel):
    vital_id: str = Field(...)
    vital_title: str = Field(...)
