from fastapi_jwt_auth.auth_jwt import uuid
from pydantic import BaseModel, Field
from typing import Optional
import time

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    password: str = Field(...)
    class Config: 
        orm_mode = True


class UserCreate(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    fullname: str = Field(...)
    account_type: str = Field(...)
    class Config: 
        orm_mode = True

class UpdateUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    fullname: Optional[str]
    account_type: Optional[str]
    
    class Config:
        orm_mode = True