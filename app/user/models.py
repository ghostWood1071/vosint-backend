from fastapi_jwt_auth.auth_jwt import uuid
from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    hashed_password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "password": "password"
            }
        }


class UserCreate(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
