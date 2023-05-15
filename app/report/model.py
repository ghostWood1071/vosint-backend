from typing import List, Optional, Any

from pydantic import BaseModel, Field


class CreateReport(BaseModel):
    title: str = Field()
    headings: Optional[Any]


class UpdateReport(BaseModel):
    title: Optional[Any] = Field(default=None, description="The title of the report")
    headings: Optional[Any]


class EventsDto(BaseModel):
    _id: str
    event_ids: List[str]


class CreateEvents(BaseModel):
    event_ids: Optional[List[str]] = Field(...)


class UpdateEvents(BaseModel):
    event_ids: Optional[List[str]] = Field(...)
