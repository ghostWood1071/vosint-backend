from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT

from .services import count_news, find_news_by_filter_and_paginate

router = APIRouter()


@router.get("/")
async def get_news(skip=0, limit=20, Authorize: AuthJWT = Depends()):
    Authorize: AuthJWT = Depends()

    news = await find_news_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_news({})
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "result": news,
                            "total_record": count
                        })
