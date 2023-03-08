from typing import Optional

from pydantic import BaseModel, Field


class CreateSocialModel(BaseModel):
    social_name: str = Field(...)
    social_media: str = Field(...)
    social_type: str = Field(...)
    account_link: str
    avatar_url: str = Field(...)
    profile: str = Field(...)
    is_active: bool = True

    class config:
        orm_mode = True


class UpdateSocial(BaseModel):
    id: Optional[str] = Field(...)
    social_name: Optional[str] = Field(...)
    social_media: Optional[str] = Field(...)
    social_type: Optional[str] = Field(...)
    account_link: Optional[str]
    avatar_url: Optional[str] = Field(...)
    profile: Optional[str] = Field(...)
    is_active: Optional[bool]


class UpdateStatus(BaseModel):
    id: Optional[str] = Field(...)
    is_active: bool = True
