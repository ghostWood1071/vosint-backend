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
    statistics_sentiments,
    collect_keyword,
    get_keyword_frequences,
    get_top_seven_by_self,
    get_top_five_by_self
)
from .utils import news_to_json
from fastapi import Response
import re
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


@router.get("/get-detail/{id}")
async def get_news_detail(id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    user = await find_user_by_id(ObjectId(user_id))
    news = await find_news_by_id(
        ObjectId(id),
    )

    if "vital_list" in user and news["_id"] in user["vital_list"]:
        news["is_bell"] = True
    if "news_bookmarks" in user and news["_id"] in user["news_bookmarks"]:
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


@router.get("/get-statistics-sentiments")
async def get_statistics_sentiments(
    text_search="",
    start_date: str = "",
    end_date: str = "",
    sac_thai: str = "",
    language_source: str = "",
    news_letter_id: str = "",
    authorize: AuthJWT = Depends(),
    vital: str = "",
    bookmarks: str = "",
    subject_id: str = None,
    newsletter_type:str = None
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    # print(user_id)
    try:
        query = {}
        query["$and"] = []
        
        if start_date != "" and end_date != "":
            start_date = datetime(
                int(start_date.split("/")[2]),
                int(start_date.split("/")[1]),
                int(start_date.split("/")[0]),
            )
            end_date = datetime(
                int(end_date.split("/")[2]),
                int(end_date.split("/")[1]),
                int(end_date.split("/")[0]),
            )

            end_date = end_date.replace(hour=23, minute=59, second=59)
            query["$and"].append({"pub_date": {"$gte": start_date, "$lte": end_date}})

        elif start_date != "":
            start_date = datetime(
                int(start_date.split("/")[2]),
                int(start_date.split("/")[1]),
                int(start_date.split("/")[0]),
            )
            query["$and"].append({"pub_date": {"$gte": start_date}})
        elif end_date != "":
            end_date = datetime(
                int(end_date.split("/")[2]),
                int(end_date.split("/")[1]),
                int(end_date.split("/")[0]),
            )
            end_date = end_date.replace(hour=23, minute=59, second=59)
            query["$and"].append({"pub_date": {"$lte": end_date}})

        if sac_thai != "" and sac_thai != "all":
            query["$and"].append({"data:class_sacthai": sac_thai})

        if language_source != "":
            language_source_ = language_source.split(",")
            language_source = []
            for i in language_source_:
                language_source.append(i)
            ls = []
            for i in language_source:
                ls.append({"source_language": i})

            query["$and"].append({"$or": ls.copy()})

        elif text_search != "":
            query["$and"].append(
                {
                    "$or": [
                        {
                            "data:content": {
                                "$regex": rf"(?<![\p{{L}}\p{{N}}]){re.escape(text_search.strip())}(?![\p{{L}}\p{{N}}])",
                                "$options": "iu",
                            }
                        },
                        {
                            "data:title": {
                                "$regex": rf"(?<![\p{{L}}\p{{N}}]){re.escape(text_search.strip())}(?![\p{{L}}\p{{N}}])",
                                "$options": "iu",
                            }
                        },
                    ]
                },
            )

    except:
        query = {}
    if str(query) == "{'$and': []}":
        query = {}
    # order="data: gtitle"
    return await statistics_sentiments(
        query,
        params={
            "text_search": text_search,
            "sentiment": sac_thai,
            "language_source": language_source,
            "start_date": start_date,
            "end_date": end_date,
            "newsletter_id": news_letter_id,
            "user_id": user_id, 
            "subject_id": subject_id,
            "vital": vital, 
            "bookmarks": bookmarks,
            "newsletter_type": newsletter_type
        },
    )


@router.post("/collect-keyword")
async def collect_keyword_route(subject_name: str = "", keywords:Any=None, collect_time:str = "",auth:AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    inserted_id = await collect_keyword(subject_name, keywords, user_id, collect_time)
    return inserted_id

@router.post("/get-keyword-frequences")
async def get_keyword_frequnences_route(start_date: str = None, end_date:str = None, top: int = 10):
    return await get_keyword_frequences(start_date, end_date, top)

# ------------ statistic news -------------------
@router.get("/get-top-seven-by-self")
async def get_top_seven_by_self_route(start_date: str = None, end_date:str = None, auth:AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    return await get_top_seven_by_self(start_date, end_date, user_id)

@router.get("/get-top-five-by-self")
async def get_top_five_by_self_route(start_date: str = None, end_date:str = None, auth:AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    return await get_top_five_by_self(start_date, end_date, user_id)

