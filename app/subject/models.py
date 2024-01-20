from pydantic import BaseModel, Field

class Subject(BaseModel):
    sub_id: str = Field(alias="_id")
    sort_order:int = 1
    name: str
    