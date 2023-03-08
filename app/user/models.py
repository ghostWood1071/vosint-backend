# from ast import List
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Role(str, Enum):
    admin = "admin"
    expert = "expert"
    leader = "leader"


class UserModal(BaseModel):
    username: str
    password: str
    full_name: str
    role: Role
    news_bookmarks: list[str]
    vital_list: list[str]
    avatar_url: Optional[str]


class UserCreateModel(BaseModel):
    username: str
    password: str
    full_name: str
    role: Role


class UserUpdateModel(BaseModel):
    username: Optional[str]
    password: Optional[str]
    full_name: Optional[str]
    role: Optional[Role]
    avatar_url: Optional[str]


class UserLoginModel(BaseModel):
    username: str
    password: str


class UserChangePasswordModel(BaseModel):
    password: str
    new_password: str
