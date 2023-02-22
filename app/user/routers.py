from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.auth.password import get_password_hash
from db.init_db import get_collection_client

from .models import UserCreateModel
from .services import (
    create_user,
    delete_bookmark_user,
    get_all_user,
    get_user,
    update_bookmark_user,
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


@router.get("/")
async def get_all():
    users = await get_all_user()
    if users:
        return users
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="List of account users is empty"
    )


@router.get("/{id}")
async def get_user_id(id):
    user = await get_user(id)
    if user:
        return user
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not exist")


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


@router.put("/add_bookmark")
async def Update_bookmark_user(
    bookmarks: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    id_obj = ObjectId(authorize.get_jwt_subject())
    list_bookmark_news = []
    for bookmark in bookmarks:
        list_bookmark_news.append(ObjectId(bookmark))
    await update_bookmark_user(id_obj, list_bookmark_news)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.put("/delete_bookmark")
async def Delete_bookmark_user(
    id_bookmarks: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    id_obj = ObjectId(authorize.get_jwt_subject())
    list_bookmark_news = []
    for id_bookmark in id_bookmarks:
        list_bookmark_news.append(ObjectId(id_bookmark))
    await delete_bookmark_user(id_obj, list_bookmark_news)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)
