from pydantic import BaseModel, Field
from bson import ObjectId

class Subject(BaseModel):
    sub_id: str = Field(default_factory=ObjectId, alias="_id")
    sort_order:int = 1
    name: str
    