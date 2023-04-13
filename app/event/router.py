from typing import List, Optional

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.event.model import AddNewEvent, CreateEvent, UpdateEvent
from app.event.service import (
    add_event,
    add_list_event_id,
    add_list_new,
    add_list_new_id,
    count_event,
    delete_event,
    delete_list_new,
    event_detail,
    get_all_by_paginate,
    remove_list_event_id,
    remove_list_new_id,
    search_event,
    search_result,
    update_event,
)
from db.init_db import get_collection_client

router = APIRouter()
client = get_collection_client("event")


@router.post("/")
async def create_event(data: CreateEvent = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    event = data.dict()
    event["user_id"] = user_id
    exist_event = await client.find_one({"event_name": event["event_name"]})
    if exist_event:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="event already exist"
        )
    event_created = await add_event(event)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=str(event_created.inserted_id)
    )


@router.put("/add-new/{id_event}")
async def add_new_list(id_event: str, list_id_new: List[str] = Body(...)):
    list_new = []
    for item in list_id_new:
        list_new.append(ObjectId(item))
    await add_list_new_id(id_event, list_id_new)
    return status.HTTP_201_CREATED


@router.put("/remove-new/{id_event}")
async def remove_new(id_event: str, list_id_new: List[str] = Body(...)):
    list_new = []
    for item in list_id_new:
        list_new.append(ObjectId(item))
    await remove_list_new_id(id_event, list_id_new)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Successful remove")


# @router.put("/add-new/")
# async def add_more_new(id_new: str, list_news: List[AddNewEvent] = Body(...)):
#     id_obj = ObjectId(id_new)
#     news = []
#     for list_new in list_news:
#         follow = AddNewEvent(
#             id_new=list_new.id_new, data_title=list_new.data_title, data_url=list_new.data_url
#         )
#         news.append(follow)
#     await add_list_new(id_obj, news)
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content="Successful add")


# @router.put("/remove-new/")
# async def remove_new(id_event: str, list_news: List[AddNewEvent] = Body(...)):
#     id_ev = ObjectId(id_event)
#     list_exist_new = []
#     for item in list_news:
#         list_exist_new.append(item)
#     await delete_list_new(id_ev, list_exist_new)
#     return JSONResponse(status_code=status.HTTP_200_OK, content="Successful remove")


@router.put("/add-event/{id_new}")
async def add_event_list(id_new: str, list_id_event: List[str] = Body(...)):
    list_new = []
    for item in list_id_event:
        list_new.append(ObjectId(item))
    await add_list_event_id(id_new, list_id_event)
    return status.HTTP_201_CREATED


@router.put("/remove-event/{id_new}")
async def remove_event(id_new: str, list_id_event: List[str] = Body(...)):
    list_event = []
    for item in list_id_event:
        list_event.append(ObjectId(item))
    await remove_list_event_id(id_new, list_id_event)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Successful remove")


@router.get("/")
async def get_all(skip=0, limit=10):
    list_event = await get_all_by_paginate({}, int(skip), int(limit))
    count = await count_event({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": list_event, "total": count}
    )


@router.get("/detail/{event_id}")
async def get_event(event_id: str):
    detail = await event_detail(event_id)
    if detail:
        return detail
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="event not exist"
    )


@router.get("/news/{news_id}")
async def show_event_by_news(news_id: str):
    result = await client.find({"new_list": news_id}).to_list(length=None)
    return result


@router.get("/search/")
async def search_by_name(event_name: Optional[str] = "", skip=0, limit=10):
    search_list = await search_event(event_name, int(skip), int(limit))
    count = await search_result(event_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": search_list, "total": count}
    )


@router.get("/filter-news/")
async def show_event(id_event: Optional[str] = ""):
    result = await client.find({"new_list": {"$nin": [id_event]}}).to_list(length=None)
    return result


@router.put("/{id}")
async def update(
    id: str, data: UpdateEvent = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    data = {k: v for k, v in data.dict().items() if v is not None}
    data["user_id"] = user_id
    updated_event = await update_event(id, data)
    if updated_event:
        return 200
    return status.HTTP_403_FORBIDDEN


@router.delete("/{id}")
async def remove_event(id):
    deleted = await delete_event(id)
    if deleted:
        return {"messsage": "event deleted successful"}
    return status.HTTP_403_FORBIDDEN
