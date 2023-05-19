from typing import Any, List, Optional

from pydantic import BaseModel, Field


class CreateReport(BaseModel):
    title: str = Field()
    headings: Optional[Any]

class GetEvents(BaseModel):
    id_linh_vuc: str
    start: Optional[str] = ""
    end: Optional[str] = ""
    count: int

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
