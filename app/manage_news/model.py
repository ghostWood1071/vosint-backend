import re
from typing import Optional

from pydantic import BaseModel, Field


class CreateSourceGroup(BaseModel):
    user_id: str
    source_name: str
    news: list[str] = []

    class config:
        orm_mode = True
        
class CreateSourceNew(BaseModel):
    name: str
    nation: str
    group: str
    url: str
    
    class config:
        orm_mode = True
    
