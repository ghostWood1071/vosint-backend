from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.event.model import CreateEvent, UpdateEvent
from app.event.service import (
    Count,
    Create_event,
    Delete_event,
    add_list_infor,
    get,
    get_all_by_paginate,
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
    await Create_event(event)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=200)

@router.post("/add-source/{id}")
async def add_infor(id: str, list_id_infor: List[str] = Body(...)):
    list_infor = []
    for item in list_id_infor:
        list_infor.append(ObjectId(item))
    await add_list_infor(id, list_id_infor)
    return status.HTTP_201_CREATED

@router.get("/")
async def get_all(skip=0, limit=10):
    list_event = await get_all_by_paginate({}, int(skip), int(limit))
    count = await Count({})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": list_event, "total": count}
    )
    
@router.put("/{id}")
async def update(id: str, data: UpdateEvent = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    all_event = await get({}) 
    data = {k: v for k, v in data.dict().items() if v is not None}
    data["user_id"] = user_id
    updated_event = await update_event(id, data, all_event)
    if updated_event:
        return 200
    return status.HTTP_403_FORBIDDEN

@router.delete("/{id}")
async def delete_event(id):
    deleted = await Delete_event(id)
    if deleted:
        return {"messsage": "event deleted successful"}
    return status.HTTP_403_FORBIDDEN
