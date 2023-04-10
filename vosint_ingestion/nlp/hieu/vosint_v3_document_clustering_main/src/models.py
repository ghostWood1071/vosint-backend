from typing import List, Optional
from pydantic import BaseModel

class News(BaseModel):
    id: str
    title: str
    content: str
    cls: Optional[str] = 'unknown'

    def __getitem__(self, item):
        return getattr(self, item)

class ListNews(BaseModel):
    data: List[News]

    def __getitem__(self, item):
        return getattr(self, item)