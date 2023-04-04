from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CreateEvent(BaseModel):
    event_name: str = Field(...)
    event_content: str = Field(...)
    start_date: Optional[str]
    end_date: Optional[str]
    new_list: List[str] = []
    system_created: bool = True
    chu_the: str
    khach_the: str
    user_id: str

    class config:
        orm_mode = True


class UpdateEvent(BaseModel):
    event_name: Optional[str] = Field(...)
    event_content: Optional[str] = Field(...)
    start_date: Optional[str]
    end_date: Optional[str]
    new_list: List[str] = []
    system_created: bool
    chu_the: str
    khach_the: str
    user_id: str
