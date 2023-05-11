from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.user.services import find_user_by_id

from .services import (
    count_news,
    find_news_by_filter_and_paginate,
    find_news_by_id,
    read_by_id,
    unread_by_id,
)
from .utils import news_to_json

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
    "keywords": True,
    "pub_date": True,
    "event_list": True,
    "is_read": True,
    "list_user_read": True
}


@router.get("/")
async def get_news(title: str = "", skip=1, limit=20, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    query = {"$or": [{"data:title": {"$regex": title, "$options": "i"}}]}
    news = await find_news_by_filter_and_paginate(
        query,
        projection,
        int(skip),
        int(limit),
    )
    count = await count_news(query)
    for item in news:
         if "is_read" not in item:
            item["is_read"] = False
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": news, "total_record": count}
    )


@router.get("/{id}")
async def get_news_detail(id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    user = await find_user_by_id(ObjectId(user_id))
    news = await find_news_by_id(
        ObjectId(id),
        projection,
    )

    if news["_id"] in user["vital_list"]:
        news["is_bell"] = True
    if news["_id"] in user["news_bookmarks"]:
        news["is_star"] = True

    return JSONResponse(status_code=status.HTTP_200_OK, content=news_to_json(news))

@router.post('/read/{id}')
async def read_id(id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    await read_by_id(id, user_id)
    return id


@router.post('/unread/{id}')
async def read_id(id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    await unread_by_id(id, user_id)
    return id
