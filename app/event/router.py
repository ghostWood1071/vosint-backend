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
    count_event_system,
    delete_event,
    delete_list_new,
    event_detail,
    event_detail_system,
    get_all_by_paginate,
    get_all_by_system,
    remove_list_event_id,
    remove_list_new_id,
    search_event,
    search_id,
    search_result,
    update_add,
    update_event,
)
from db.init_db import get_collection_client

router = APIRouter()
client = get_collection_client("event")
client3 = get_collection_client("event_system")

@router.get("/all-system-created/")
async def get_all(skip=1, limit=10):
    list_event = await get_all_by_system({}, int(skip), int(limit))
    count = await count_event_system({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": list_event, "total": count}
    )
    
@router.post("/")
async def create_event(data: CreateEvent = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    event = data.dict()
    event["user_id"] = user_id
    if event["system_created"] == True:
        exist_event_system = await client3.find_one({"event_name": event["event_name"]})
        event["user_id"] = 0
        if exist_event_system:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="event already exist"
            )
    if event["system_created"] == False:
        exist_event = await client.find_one({"event_name": event["event_name"]})
        if exist_event:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="event already exist"
            )
    event["total_new"] = len(event["new_list"])
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
async def remove_new_list(id_event: str, list_id_new: List[str] = Body(...)):
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
async def remove_event_list(id_new: str, list_id_event: List[str] = Body(...)):
    list_event = []
    for item in list_id_event:
        list_event.append(ObjectId(item))
    await remove_list_event_id(id_new, list_id_event)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Successful remove")


@router.get("/")
async def get_all(skip=1, limit=10):
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

@router.get("/detail-system/{event_id}")
async def get_event(event_id: str):
    detail = await event_detail_system(event_id)
    if detail:
        return detail
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="event not exist"
    )

@router.get("/news/{news_id}")
async def show_event_by_news(news_id: str):
    result = await client.find({"new_list": news_id}).to_list(length=None)
    for item in result:
        item["total_new"] = len(item["new_list"])
    return result

@router.get("/news/system/{news_id}")
async def show_event_by_news_and_system(news_id: str):
    result = await client3.find({"new_list": news_id}).to_list(length=None)
    for item in result:
        item["total_new"] = len(item["new_list"])
    return result


@router.get("/search/")
async def search_by_name(
    event_name: Optional[str] = "", 
    id_new: Optional[str] = "", 
    chu_the: Optional[str] = "", 
    khach_the: Optional[str] = "",
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
    skip=1, 
    limit=10
):
    search_list = await search_event(event_name, id_new, chu_the, khach_the, start_date, end_date, int(skip), int(limit))
    count = await search_result(event_name, id_new, chu_the, khach_the, start_date, end_date)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": search_list, "total": count}
    )
    
@router.get("/search-based-user-id/")
async def search_based_id_system(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    search_list = await search_id(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": search_list})

@router.put("/update-to-add/{id}")
async def update_to_add(id: str, data: UpdateEvent = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    created = data.dict()
    if created["system_created"] == True:
        created["user_id"] = 0
    if created["system_created"] == False:
        created["user_id"] = user_id
    await update_add(id, created)
    return 200
    
@router.put("/{id}")
async def update(
    id: str, data: UpdateEvent = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    data = {k: v for k, v in data.dict().items() if v is not None}
    if data["system_created"] == True:
        data["user_id"] = 0
    if data["system_created"] == False:
        data["user_id"] = user_id
    data["total_new"] = len(data["new_list"])
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
