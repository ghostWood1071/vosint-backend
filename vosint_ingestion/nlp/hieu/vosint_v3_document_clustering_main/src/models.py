from typing import List

from pydantic import BaseModel


class News(BaseModel):
    class_name: str
    van_ban_mau: List[str]
    vocab: List[str]
