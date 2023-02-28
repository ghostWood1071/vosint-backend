from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from app.user.models import Role


class UserModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    username: str = Field(...)
    hash_password: str = Field(...)
    social: str
    users_follow: List[str]


class UserCreateModel(BaseModel):
    username: str
    password: str
    social: str
    users_follow: List[str]
