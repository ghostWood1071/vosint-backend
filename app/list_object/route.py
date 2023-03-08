from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse

from app.list_object.model import CreateObject, UpdateObject
from app.list_object.service import (
    count_all_object,
    count_object,
    count_search_object,
    create_object,
    delete_object,
    find_by_filter_and_paginate,
    get_all_object,
    search_by_filter_and_paginate,
    update_object,
)
from db.init_db import get_collection_client

router = APIRouter()

db = get_collection_client("object")


@router.post("/")
async def add_object(
    payload: CreateObject, 
    type: Optional[str] = Query("Type", enum = ["Đối tượng", "Tổ chức", "Quốc gia"]),
    Status: Optional[str] = Query("Status", enum = ["enable", "disable"])
):
    object = payload.dict()
    exist_object = await db.find_one({"name": object["name"]})
    if exist_object:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="object already exist"
        )
        
    object["type"] = type
    object["status"] = Status
    
    new_object = await create_object(object)
    return new_object

# @router.get("/{type}")
# async def get_search(type: str = Path(..., title="Object type", enum = ["Đối tượng", "Tổ chức", "Quốc gia"]), skip = 0, limit = 10):
#     search_object = await search_by_filter_and_paginate(type, int(skip), int(limit))
#     Count = await count_search_object(type)
#     return JSONResponse(
#         status_code=status.HTTP_200_OK, content={"data": search_object, "total": Count}
#     )


# @router.get("/")
# async def get_all(skip=0, limit=10):
#     list = await get_all_object({}, int(skip), int(limit))
#     all = await count_all_object({})
#     return {"result": list, "total": all}

@router.get("/{type}")
async def get_type_and_name(
    name: str = "",
    type: Optional[str] = Path(..., title="Object type", enum = ["Đối tượng", "Tổ chức", "Quốc gia"]), 
    skip = 0, 
    limit = 10
):
    list_obj = await find_by_filter_and_paginate(name, type, int(skip), int(limit))
    count = await count_object(type)
    return {"data": list_obj, "total": count}


@router.put("/{id}")
async def update_one(id, data: UpdateObject = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_object = await update_object(id, data)
    if updated_object:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.delete("/{id}")
async def delete_one(id):
    deleted_object = await delete_object(id)
    if deleted_object:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
