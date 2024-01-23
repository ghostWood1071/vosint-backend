from typing import Optional

from fastapi import APIRouter, Body
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
import re

from db.init_db import get_collection_client

from .model import CreateReport, UpdateReport, Heading, NewsParams
from .service import (
    add_heading_to_report,
    count,
    create_report,
    delete_report,
    get_report,
    get_reports,
    remove_heading_from_report,
    update_report,
    add_news_to_heading,
    remove_news_from_heading
)

event_client = get_collection_client("event")

router = APIRouter()
 

#-
# get report list
@router.get("")
async def read_reports(
    title: str = "", skip: int = 0, limit: int = 10, auth: AuthJWT = Depends()
):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()

    query = {
        # "$text": {"$search": title},
        "user_id": user_id,
    }
    if title != "":
        query["$text"] = {"$search": title}

    reports = await get_reports(query, skip, limit)
    reports_count = await count(query)

    return {
        "data": reports,
        "total": reports_count,
    }

#get report detail
@router.get("/{id}")
async def read_report(id: str, auth: AuthJWT = Depends()):
    auth.jwt_required()
    report = await get_report(id)
    return report

# add new report 
@router.post("")
async def post_report(report: CreateReport = Body(...), auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    report_dict = report.dict()
    report_dict["user_id"] = user_id
    report_dict["news_ids"] = []
    report_created = await create_report(report_dict)
    return report_created.inserted_id

#update report
@router.put("/{id}")
async def put_report(id: str, data: UpdateReport = Body(...), auth: AuthJWT = Depends()):
    auth.jwt_required()
    report_dict = {k: v for k, v in data.dict().items() if v is not None}
    await update_report(id, report_dict)
    return id

#delete report
@router.delete("/{id}")
async def delete(id: str, auth: AuthJWT = Depends()):
    auth.jwt_required()
    await delete_report(id)
    return id
#----------------------------------------------------------------------------------------------
#add an event to heading
@router.post("/add-heading")
async def add_heading(heading: Heading, auth: AuthJWT = Depends()):
    auth.jwt_required()
    await add_heading_to_report(heading.dict())
    return 200

# remove a heading
@router.post("/remove-heading/")
async def delete_heading(id_report: Optional[str] = "", id_heading: Optional[str] = "", auth: AuthJWT = Depends()):
    auth.jwt_required()
    await remove_heading_from_report(id_report, id_heading)
    return 200

#-----------------------------------------------------------------------------------------------
@router.post("/add-news-to-heading")
async def add_news_to_heading_route(data: NewsParams, auth: AuthJWT = Depends()):
    auth.jwt_required()
    await add_news_to_heading(**data.dict())


@router.post("/remove-news-from-heading")
async def remove_news_from_heading_route(data: NewsParams, auth: AuthJWT = Depends()):
    auth.jwt_required()
    await remove_news_from_heading(**data.dict())