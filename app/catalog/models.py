from pydantic import BaseModel, Field
from bson import ObjectId

class Catalog(BaseModel):
    catalog_id: str = Field(default_factory=ObjectId, alias="_id")
    catalog_name: str
    catalog_description: str
    picture: str
    sort_order: int = 1

