from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AddNewEvent(BaseModel):
    id_new: str
    data_title: str 
    data_url: str 

class CreateEvent(BaseModel):
    event_name: str = Field(...)
    event_content: str = Field(...)
    date_created: str
    new_list: List[str] = []
    system_created: bool = True
    chu_the: str
    khach_the: str
    user_id: Optional[str]

    class config:
        orm_mode = True

class UpdateEvent(BaseModel):
    event_name: Optional[str] = Field(...)
    event_content: Optional[str] = Field(...)
    date_created: Optional[str] = Field(...)
    new_list: List[str] = []
    system_created: bool = True
    chu_the: str
    khach_the: str
    user_id: Optional[str]
