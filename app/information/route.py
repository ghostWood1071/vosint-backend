from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse

from app.information.model import CreateInfor, UpdateInfor
from app.information.service import (
    count_infor,
    count_search_infor,
    create_infor,
    delete_infor,
    find_by_filter_and_paginate,
    get_all_infor,
    search_by_filter_and_paginate,
    search_infor,
    update_infor,
)
from db.init_db import get_collection_client

router = APIRouter()
infor_collect = get_collection_client("infor")


@router.post("/")
async def add_infor(payload: CreateInfor):
    infor = payload.dict()
    exist_infor = await infor_collect.find_one({"name": infor["name"]})
    if exist_infor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="infor already exist"
        )
    new_infor = await create_infor(infor)
    return new_infor


# @router.post("/add-infor/{name}")
# async def add_news(name: str, payload: CreateInfor = Body(...)):
#     Payload = payload.dict()
#     await add_list_infor(name, Payload)
#     return status.HTTP_201_CREATED


@router.get("/")
async def get_all(skip = 0, limit = 10):
    list_infor = await find_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_infor({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": list_infor, "total_record": count}
    )

@router.get("/{name}")
async def search(name, skip = 0, limit = 10):
    list_infor = await search_by_filter_and_paginate(name, int(skip), int(limit))
    count = await count_search_infor(name)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": list_infor, "total_record": count}
    )

@router.put("/{id}")
async def update(id, data: UpdateInfor = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_infor = await update_infor(id, data)
    if updated_infor:
        return status.HTTP_200_OK
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="update unsuccessful"
    )


@router.delete("/{id}")
async def delete(id):
    deleted_infor = await delete_infor(id)
    if deleted_infor:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
