from typing import Annotated, List, Optional

from bson.objectid import ObjectId
from fastapi import APIRouter, Body
from fastapi_jwt_auth import AuthJWT

from .model import CreateReport, UpdateReport, CreateEvents, UpdateEvents
from .service import (
    count,
    create_report,
    delete_report,
    get_reports,
    get_report,
    update_report,
    get_events,
    create_events,
    update_events,
    add_event_ids_to_events,
    remove_event_ids_in_events,
)

router = APIRouter()


@router.get("/")
async def read_reports(title: str = "", skip: int = 0, limit: int = 10):
    query = {
        "$or": [
            {"title": {"$regex": title, "$options": "i"}},
        ]
    }

    reports = await get_reports(query, skip, limit)
    reports_count = await count(query)
    return {
        "data": reports,
        "total": reports_count,
    }


@router.get("/{id}")
async def read_report(id: str):
    report = await get_report(id)
    return report


@router.post("/")
async def post_report(report: CreateReport = Body(...)):
    report_dict = report.dict()
    report_created = await create_report(report_dict)
    return report_created.inserted_id


@router.put("/{id}")
async def put_report(id: str, data: UpdateReport = Body(...)):
    report_dict = {k: v for k, v in data.dict().items() if v is not None}
    await update_report(id, report_dict)
    return id


@router.delete("/{id}")
async def delete_report(id: str):
    await delete_report(id)
    return id


@router.get("/events/{id}")
async def read_event(id: str):
    event = await get_events(id)
    return event


@router.post("/events")
async def post_event(event: CreateEvents = Body(...)):
    event_dict = event.dict()
    event_created = await create_events(event_dict)
    return event_created.inserted_id


@router.put("/events/{id}")
async def put_event(id: str, data: UpdateEvents = Body(...)):
    event_dict = {k: v for k, v in data.dict().items() if v is not None}
    await update_events(id, event_dict)
    return id


@router.delete("/events/{id}")
async def delete_event(id: str):
    await delete_event(id)
    return id


@router.post("/events/{id}/add_event_ids")
async def add_event_ids(id: str, event_ids: List[str]):
    await add_event_ids_to_events(id, event_ids)
    return id


@router.post("/events/{id}/remove_event_ids")
async def remove_event_ids(id: str, event_ids: List[str]):
    await remove_event_ids_in_events(id, event_ids)
    return id
