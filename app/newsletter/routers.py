from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.params import Body, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.news.services import (
    count_news,
    find_news_by_filter,
    find_news_by_filter_and_paginate,
)

from .models import NewsLetterCreateModel, NewsLetterUpdateModel, NewsletterDeleteMany
from .services import (
    create_news_ids_to_newsletter,
    create_newsletter,
    delete_news_ids_in_newsletter,
    delete_newsletter,
    find_newsletter_by_id,
    find_newsletters_and_filter,
    update_newsletter,
    delete_many_newsletter,
)
from .utils import newsletter_to_json, newsletter_to_object_id

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
async def read(title: str = "", authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    if user_id is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Bad jwt")

    query = {
        "$or": [
            {"title": {"$regex": f"\\b{title}\\b", "$options": "i"}},
            {"title": {"$regex": title, "$options": "i"}},
        ],
        "user_id": ObjectId(user_id),
    }
    newsletters = await find_newsletters_and_filter(query)

    return JSONResponse(status_code=status.HTTP_200_OK, content=newsletters)


@router.get("/{newsletter_id}/news")
async def get_news_by_newsletter_id(
    newsletter_id: str, skip=0, limit=20, authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    newsletter = await find_newsletter_by_id(ObjectId(newsletter_id))
    if newsletter is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    if "news_id" not in newsletter:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    news = await find_news_by_filter_and_paginate(
        {"_id": {"$in": newsletter["news_id"]}}, int(skip), int(limit)
    )

    count = await count_news({"_id": {"$in": newsletter["news_id"]}})

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": news, "total_record": count}
    )


@router.get("/{newsletter_id}")
async def get_details_newsletter(newsletter_id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    newsletter = await find_newsletter_by_id(
        ObjectId(newsletter_id), {"news_id": False}
    )

    if newsletter is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    news_samples = []
    if "news_samples" in newsletter:
        news_samples = await find_news_by_filter(
            {"_id": {"$in": newsletter["news_samples"]}}
        )

        newsletter["news_samples"] = news_samples

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=newsletter_to_json(newsletter)
    )


@router.delete("/{newsletter_id}")
async def delete(newsletter_id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    await delete_newsletter(ObjectId(newsletter_id))

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.post("/delete-many")
async def delete_many_by_id(body: NewsletterDeleteMany, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    filter = {"_id": {"$in": list(map(lambda x: ObjectId(x), body.newsletter_ids))}}

    await delete_many_newsletter(filter)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.put(
    "/{newsletter_id}/news",
)
async def delete_news_in_newsletter(
    newsletter_id: str, news_ids: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    news_object_ids = []
    for news_id in news_ids:
        # TODO: validate exists news
        news_object_ids.append(ObjectId(news_id))

    await delete_news_ids_in_newsletter(ObjectId(newsletter_id), news_object_ids)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.patch("/{newsletter_id}")
async def update(
    newsletter_id: str, body: NewsLetterUpdateModel, authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    parsed_newsletter = newsletter_to_object_id(body.dict())
    await update_newsletter(ObjectId(newsletter_id), parsed_newsletter)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.post("/{newsletter_id}/news")
async def add_news_ids_to_newsletter(
    newsletter_id: str, news_ids: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    newsletter_object_id = ObjectId(newsletter_id)
    news_object_ids = []
    for news_id in news_ids:
        # TODO: validate exists news
        news_object_ids.append(ObjectId(news_id))

    await create_news_ids_to_newsletter(newsletter_object_id, news_object_ids)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)
