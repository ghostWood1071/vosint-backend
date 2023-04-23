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


class EventsDto(BaseModel):
    _id: str
    event_ids: List[str]


class CreateEvents(BaseModel):
    event_ids: Optional[List[str]] = Field(...)


class UpdateEvents(BaseModel):
    event_ids: Optional[List[str]] = Field(...)
