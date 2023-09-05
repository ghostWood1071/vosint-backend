from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from app.user.services import find_user_by_id
from typing import *
from datetime import datetime
from .services import (
    count_news,
    find_news_by_filter_and_paginate,
    find_news_by_id,
    read_by_id,
    unread_news,
    find_news_by_ids,
    check_news_contain_keywords,
    remove_news_from_object,
    add_news_to_object,
)
from .utils import news_to_json
from fastapi import Response

from word_exporter import export_news_to_words

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
    "data:class_linhvuc": True,
    "created_at": True,
    "modified_at": True,
    "keywords": True,
    "pub_date": True,
    "event_list": True,
    "is_read": True,
    "list_user_read": True,
}


@router.get("")
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


@router.post("/read")
async def read_id(news_ids: List[str], authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    await read_by_id(news_ids, user_id)
    return news_ids


@router.post("/unread")
async def read_id(news_ids: List[str], authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    await unread_news(news_ids, user_id)
    return news_ids


@router.post("/export-to-word")
async def export_to_word(ids: List[str]):
    news = await find_news_by_ids(
        ids,
        {
            "data:title": 1,
            "pub_date": 1,
            "data:content": 1,
            "source_host_name": 1,
            "data:url": 1,
        },
    )
    file_buff = export_news_to_words(news)

    now_str = datetime.now().strftime("%d-%m-%Y")
    return Response(
        file_buff.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Access-Control-Expose-Headers": "Content-Disposition",
            "Content-Disposition": f"attachment; filename=tin({now_str}).docx",
        },
    )


@router.post("/check-news-contain-keywords")
def check_news_contain(
    object_ids: List[str], news_ids: List[str], new_keywords: List[str] = []
):
    return check_news_contain_keywords(object_ids, news_ids, new_keywords)


@router.post("/remove-news-from-object")
def remove_news_from_objects(object_ids: List[str], news_ids: List[str]):
    remove_news_from_object(news_ids, object_ids)
    return JSONResponse({"result": "updated sucess"}, 200)


@router.post("/add-news-to-object")
def add_news_to_objects(object_ids: List[str], news_ids: List[str]):
    result = add_news_to_object(object_ids, news_ids)
    return JSONResponse({"result": "updated sucess"}, 200)
