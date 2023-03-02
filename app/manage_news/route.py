from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.manage_news.model import CreateSourceGroup, CreateSourceNew
from app.manage_news.service import (
    add_list_infor,
    count_source,
    create_source_group,
    delete_list_infor,
    delete_source_group,
    find_by_filter_and_paginate,
    get_all_source,
)
from db.init_db import get_collection_client

router = APIRouter()

db = get_collection_client("Source")


@router.post("/")
async def add_source(payload: CreateSourceGroup):
    source = payload.dict()
    exist_source = await db.find_one({"source_name": source["source_name"]})
    if exist_source:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="source already exist"
        )
    new_source = await create_source_group(source)
    return new_source


@router.get("/")
async def get_all(skip=0, limit=10):
    list_source_group = await find_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_source({})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": list_source_group, "total_record": count},
    )


# @router.post("/add-infor/{name}")
# async def add_news(name: str, payload: CreateSourceNew = Body(...)):
#     Payload = payload.dict()
#     await update_news(name, Payload)
#     return status.HTTP_201_CREATED


@router.post("/add-infor/{name}")
async def add_infor(name: str, list_id_infor: List[str] = Body(...)):
    list_infor = []
    for item in list_id_infor:
        list_infor.append(ObjectId(item))
    await add_list_infor(name, list_id_infor)
    return status.HTTP_201_CREATED


@router.put("/delete-infor/{name}")
async def delete_infor(name: str, list_id_infor: List[str] = Body(...)):
    list_infor = []
    for item in list_id_infor:
        list_infor.append(ObjectId(item))
    await delete_list_infor(name, list_id_infor)
    return status.HTTP_201_CREATED


@router.delete("/{id}")
async def delete_source(id):
    Deleted_group_source = await delete_source_group(id)
    if Deleted_group_source:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
