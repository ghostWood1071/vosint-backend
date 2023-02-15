from enum import Enum
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = "admin"
    expert = "expert"
    leader = "leader"


class UserModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    username: str = Field(...)
    hash_password: str = Field(...)


class UserCreateModel(BaseModel):
    username: str
    password: str
    full_name: str
    role: Role


class UserUpdateModel(BaseModel):
    fullname: Optional[str]


class UserLoginModel(BaseModel):
    username: str
    password: str
