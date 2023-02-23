from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.auth.password import get_password_hash
from app.news.services import count_news, find_news_by_filter_and_paginate
from db.init_db import get_collection_client

from .models import UserCreateModel
from .services import (
    create_user,
    delete_bookmark_user,
    delete_vital_user,
    find_user_by_id,
    get_all_user,
    get_user,
    get_vital_ids,
    update_bookmark_user,
    update_vital_user,
    user_entity,
)

router = APIRouter()
"""
    Required Authorization
"""

client = get_collection_client("users")


@router.post("/")
async def add(body: UserCreateModel):
    user_dict = body.dict()

    existing_user = await client.find_one({"username": user_dict["username"]})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist"
        )

    user_dict["hashed_password"] = get_password_hash(user_dict["password"])
    user_dict.pop("password")
    await create_user(user_dict)
    return HTTPException(status_code=status.HTTP_200_OK)


@router.get("/me")
async def get_me(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await find_user_by_id(ObjectId(user_id))
    if user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=None)

    return JSONResponse(status_code=status.HTTP_200_OK, content=user_entity(user))


@router.get("/get_vital_ids")
async def get_vital_ids_by_user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await get_user(user_id)
    if user is None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"result": []})

    if "vital_list" not in user:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"result": []})

    vital_ids = await get_vital_ids(user_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": vital_ids})


@router.get("/get_vital_list")
async def get_vital_by_user(skip=0, limit=20, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await get_user(user_id)
    if user is None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"result": []})

    if "vital_list" not in user:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"result": []})

    news = await find_news_by_filter_and_paginate(
        {"_id": {"$in": user["vital_list"]}}, int(skip), int(limit)
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": news})


# @router.get("/{id}")
# async def get_user_id(id):
#     user = await get_user(id)
#     if user:
#         return user
#     return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not exist")


# @router.put('/{id}')
# async def update_user(id: str, user_data: UserUpdateModel = Body(...)):
#     user_data = {k: v for k, v in user_data.dict().items() if v is not None}
#     updated_user = await update_user(id, user_data)
#     if updated_user:
#         return updated_user
#     return status.HTTP_403_FORBIDDEN


# @router.delete('/{id}')
# async def delete_user(id: str):
#     deleted_user = await delete_user(id)
#     if deleted_user:
#         return status.HTTP_200_OK
#     return status.HTTP_403_FORBIDDEN


@router.get("/bookmarks")
async def get_news_bookmarks(skip=0, limit=20, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await find_user_by_id(ObjectId(user_id))

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    if "news_bookmarks" not in user:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    news = await find_news_by_filter_and_paginate(
        {"_id": {"$in": user["news_bookmarks"]}}, int(skip), int(limit)
    )

    count = await count_news({"_id": {"$in": user["news_bookmarks"]}})

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": news, "total_record": count}
    )


@router.post("/bookmarks")
async def add_news_to_bookmarks(
    bookmarks: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    id_obj = ObjectId(authorize.get_jwt_subject())
    list_bookmark_news = []
    for bookmark in bookmarks:
        list_bookmark_news.append(ObjectId(bookmark))
    await update_bookmark_user(id_obj, list_bookmark_news)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.put("/bookmarks")
async def delete_news_in_bookmarks(
    id_bookmarks: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    id_obj = ObjectId(authorize.get_jwt_subject())
    list_bookmark_news = []
    for id_bookmark in id_bookmarks:
        list_bookmark_news.append(ObjectId(id_bookmark))
    await delete_bookmark_user(id_obj, list_bookmark_news)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.post("/add_vital")
async def add_vital(vitals: List[str] = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    list_vitals_news = []
    for vital in vitals:
        list_vitals_news.append(ObjectId(vital))
    await update_vital_user(user_id, list_vitals_news)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.put("/delete_vital")
async def delete_vital(
    id_vitals: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    list_vitals_news = []
    for id_vital in id_vitals:
        list_vitals_news.append(ObjectId(id_vital))
    await delete_vital_user(user_id, list_vitals_news)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


# @router.get("/{id}/get_vital_list")
# async def get_vital_by_user(
#     skip=0, limit=20, authorize: AuthJWT = Depends()
# ):
#     authorize.jwt_required()
#     user_id = authorize.get_jwt_subject()
#     user = await get_user(user_id)
#     if user is None:
#         return JSONResponse(
#             status_code=status.HTTP_200_OK, content={"result": []}
#         )

#     if "vital_list" not in user:
#         return JSONResponse(
#             status_code=status.HTTP_200_OK, content={"result": []}
#         )

#     news = await find_news_by_filter_and_paginate(
#         {"_id": {"$in": user["vital_list"]}}, int(skip), int(limit)
#     )

#     return JSONResponse(
#         status_code=status.HTTP_200_OK, content={"result": news}
#     )
