# from ast import List
from enum import Enum
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = "admin"
    expert = "expert"
    leader = "leader"

class BookMarkBase(BaseModel):
    id: str = Field(...)

class UserCreateModel(BaseModel):
    username: str
    password: str
    full_name: str
    role: Role

class UserUpdateModel(BaseModel):
    username: str
    password: str
    full_name: str


class UserLoginModel(BaseModel):
    username: str
    password: str
