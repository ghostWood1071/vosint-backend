from typing import Annotated, List, Optional

from bson.objectid import ObjectId
from fastapi import APIRouter, Body
from fastapi_jwt_auth import AuthJWT

from .model import CreateEvents, CreateReport, GetEvents, UpdateEvents, UpdateReport
from .service import (
    count,
    create_report,
    delete_report,
    get_event,
    get_report,
    get_reports,
    update_report,
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
async def delete(id: str):
    await delete_report(id)
    return id

@router.post("/get-event-with-new/")
async def get_event_route(id_count: List[GetEvents] = Body(...)):
    list_ev = []
    for item in id_count:
        list_ev.append(item)
    reports = await get_event(list_ev)
    return reports
