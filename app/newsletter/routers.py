from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.params import Body, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from app.news.services import count_news, find_news_by_filter_and_paginate
from .models import NewsLetterCreateModel, NewsLetterUpdateModel
from .services import (create_news_ids_to_newsletter, create_newsletter,
                       delete_newsletter, find_newsletter_by_id,
                       find_newsletters_and_filter, update_newsletter,
                       update_newsletter_news_list)
from .utils import newsletter_to_object_id

router = APIRouter()


@router.post("/")
async def create(body: NewsLetterCreateModel, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    newsletter_dict = body.dict()
    newsletter_dict["user_id"] = user_id
    await create_newsletter(newsletter_to_object_id(newsletter_dict))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.get("/")
async def read(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    newsletters = await find_newsletters_and_filter(
        {"user_id": ObjectId(user_id)})

    return JSONResponse(status_code=status.HTTP_200_OK, content=newsletters)


@router.get("/{newsletter_id}/news")
async def get_news_by_newsletter_id(newsletter_id: str,
                                    skip=0,
                                    limit=20,
                                    authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    newsletter = await find_newsletter_by_id(ObjectId(newsletter_id))
    if "news_id" not in newsletter:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "result": [],
                                "total_record": 0
                            })

    news = await find_news_by_filter_and_paginate(
        {"_id": {
            "$in": newsletter["news_id"]
        }}, int(skip), int(limit))

    count = await count_news({"_id": {"$in": newsletter["news_id"]}})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "result": news,
                            "total_record": count
                        })


@router.delete("/{newsletter_id}")
async def delete(newsletter_id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    await delete_newsletter(ObjectId(newsletter_id))

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.delete(
    "/{newsletter_id}/news/{news_id}", )
async def delete_news_in_newsletter(newsletter_id: str,
                                    news_id: str,
                                    authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    # TODO: validate exists newsleter of user
    await update_newsletter_news_list(ObjectId(newsletter_id),
                                      ObjectId(news_id))
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.patch("/{newsletter_id}")
async def update(newsletter_id: str,
                 body: NewsLetterUpdateModel,
                 authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    parsed_newsletter = newsletter_to_object_id(body.dict())
    await update_newsletter(ObjectId(newsletter_id), parsed_newsletter)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.post("/{newsletter_id}/news")
async def add_news_ids_to_newsletter(newsletter_id: str,
                                     news_ids: List[str] = Body(...),
                                     authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    newsletter_object_id = ObjectId(newsletter_id)
    news_object_ids = []
    for news_id in news_ids:
        # TODO: validate exists news
        news_object_ids.append(ObjectId(news_id))

    await create_news_ids_to_newsletter(newsletter_object_id, news_object_ids)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)
