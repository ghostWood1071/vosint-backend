from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.user.models import Role


class UserModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    username: str = Field(...)
    hash_password: str = Field(...)
    social: str


class AddFollow(BaseModel):
    follow_id: str
    social_name: str


class AddProxy(BaseModel):
    proxy_id: str
    name: str


class UserCreateModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    social: str = Field(...)
    users_follow: List[AddFollow]
    list_proxy: List[AddProxy]


class UpdateAccountMonitor(BaseModel):
    id: str
    username: str = Field(...)
    password: str = Field(...)
    social: str = Field(...)
    users_follow: List[AddFollow]
    list_proxy: List[AddProxy]
