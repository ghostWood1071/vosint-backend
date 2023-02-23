from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.user.services import find_user_by_id

from .services import count_news, find_news_by_filter_and_paginate, find_news_by_id

router = APIRouter()


@router.get("/")
async def get_news(skip=0, limit=20, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    news = await find_news_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_news({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": news, "total_record": count}
    )


@router.get("/{id}")
async def get_news_detail(id: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    news = await find_news_by_id(ObjectId(id))
    return JSONResponse(status_code=status.HTTP_200_OK, content=news)
