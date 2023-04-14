from typing import List, Optional

from pydantic import BaseModel, Field


class CreateReport(BaseModel):
    title: str = Field()
    content: str = Field()


class UpdateReport(BaseModel):
    title: Optional[str] = Field(default=None, description="The title of the report")
    content: Optional[str] = Field(
        default=None, description="The content of the report"
    )
