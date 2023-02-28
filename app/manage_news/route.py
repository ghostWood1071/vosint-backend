from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT

from app.manage_news.model import CreateSourceGroup, CreateSourceNew
from app.manage_news.service import (
    add_list_infor,
    create_source_group,
    delete_list_infor,
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
async def get_all():
    list_source_group = await get_all_source()
    if list_source_group:
        return list_source_group
    return None


# @router.post("/add-infor/{name}")
# async def add_news(name: str, payload: CreateSourceNew = Body(...)):
#     Payload = payload.dict()
#     await update_news(name, Payload)
#     return status.HTTP_201_CREATED


@router.post("/add-infor/{name}")
async def add_news(name: str, list_id_infor: List[str] = Body(...)):
    list_infor = []
    for item in list_id_infor:
        list_infor.append(ObjectId(item))
    await add_list_infor(name, list_id_infor)
    return status.HTTP_201_CREATED


@router.put("/delete-infor/{name}")
async def add_news(name: str, list_id_infor: List[str] = Body(...)):
    list_infor = []
    for item in list_id_infor:
        list_infor.append(ObjectId(item))
    await delete_list_infor(name, list_id_infor)
    return status.HTTP_201_CREATED
