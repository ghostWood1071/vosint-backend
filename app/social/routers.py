from typing import List

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.auth.password import get_password_hash
from app.social.models import UserCreateModel
from app.social.services import (
    create_user,
    delete_follow_user,
    delete_user,
    get_all_user,
    get_user,
    update_follow_user,
    update_username_user,
)
from db.init_db import get_collection_client

client = get_collection_client("socials")

router = APIRouter()


@router.get("/")
async def Get_all_user(skip: int, limit: int):
    users = await get_all_user(skip, limit)
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


@router.post("/")
async def add_user(
    body: UserCreateModel, _q: str = Query("Social", enum=["Facebook", "Twitter"])
):
    user_dict = body.dict()
    existing_user = await client.find_one({"username": user_dict["username"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist"
        )
    user_dict["hashed_password"] = get_password_hash(user_dict["password"])
    user_dict.pop("password")
    user_dict["social"] = _q
    user_dict["users_follow"] = []
    await create_user(user_dict)
    return HTTPException(status_code=status.HTTP_200_OK)


@router.delete("/{id}")
async def Delete_user(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.put("/update_username")
async def Update_username_user(id_user: str, username_new: str):
    id_obj = ObjectId(id_user)
    await update_username_user(id_obj, username_new)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.put("/add_follow")
async def Update_follow_user(id_user: str, id_users_follow: List[str] = Body(...)):
    id_obj = ObjectId(id_user)
    list_id_new = []
    for id_user in id_users_follow:
        list_id_new.append(ObjectId(id_user))
    await update_follow_user(id_obj, list_id_new)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.put("/delete_follow")
async def Delete_follow_user(id_user: str, id_users_follow: List[str] = Body(...)):
    id_obj = ObjectId(id_user)
    list_id_new = []
    for id_user in id_users_follow:
        list_id_new.append(ObjectId(id_user))
    await delete_follow_user(id_obj, list_id_new)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)
