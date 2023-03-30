from typing import Optional

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.list_object.model import CreateObject, UpdateObject
from app.list_object.service import (
    count_all_object,
    count_object,
    count_search_object,
    create_object,
    delete_object,
    find_by_filter_and_paginate,
    find_by_id,
    get_all_object,
    search_by_filter_and_paginate,
    update_object,
)
from app.news.services import (
    count_news,
    find_news_by_filter,
    find_news_by_filter_and_paginate,
)
from db.init_db import get_collection_client

router = APIRouter()

projection = {
    "data:title": True,
    "data:html": True,
    "data:author": True,
    "data:time": True,
    "data:content": True,
    "data:url": True,
    "data:class": True,
    "data:class_sacthai": True,
    "created_at": True,
    "modified_at": True,
}

db = get_collection_client("object")


@router.post("/")
async def add_object(
    payload: CreateObject,
    type: Optional[str] = Query("Type", enum=["Đối tượng", "Tổ chức", "Quốc gia"]),
    Status: Optional[str] = Query("Status", enum=["enable", "disable"]),
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


@router.get("/{Type}")
async def get_type_and_name(
    name: str = "",
    Type: Optional[str] = Path(
        ..., title="Object type", enum=["Đối tượng", "Tổ chức", "Quốc gia"]
    ),
    skip=0,
    limit=10,
):
    list_obj = await find_by_filter_and_paginate(name, Type, int(skip), int(limit))
    count = await count_object(Type, name)
    return {"data": list_obj, "total": count}


@router.get("/{id}/news")
async def get_news_by_object_id(
    id: str, skip=0, limit=20, authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    # pipeline = [
    #     {"$match": {"_id": ObjectId(id)}},
    #     {
    #         "$addFields": {
    #             "news_id": {
    #                 "$map": {
    #                     "input": "$news_id",
    #                     "as": "id",
    #                     "in": {"$toString": "$$id"},
    #                 }
    #             }
    #         }
    #     },
    #     {"$project": {"news_id": 1}},
    # ]
    # object = await aggregate_object(pipeline)
    object = await find_by_id(ObjectId(id), {"news_id": 1})
    if "news_id" not in object:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    news = await find_news_by_filter_and_paginate(
        {"_id": {"$in": object["news_id"]}}, projection, int(skip), int(limit)
    )
    count = await count_news({"_id": {"$in": object["news_id"]}})

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": news, "total_record": count}
    )


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
