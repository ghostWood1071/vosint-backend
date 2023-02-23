from typing import Optional

from pydantic import BaseModel, Field


class CreateInfor(BaseModel):
    infor_name: str
    host_name: str
    language: str
    publishing_country: str
    source_type: str

    class config:
        orm_mode = True


class UpdateInfor(BaseModel):
    infor_name: Optional[str]
    host_name: Optional[str]
    language: Optional[str]
    publishing_country: Optional[str]
    source_type: Optional[str]

    class config:
        orm_mode = True
