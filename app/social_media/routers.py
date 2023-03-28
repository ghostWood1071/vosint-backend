from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Path, status
from fastapi.responses import JSONResponse

from db.init_db import get_collection_client

from .models import AddFollowed, CreateSocialModel, UpdateSocial, UpdateStatus
from .services import (
    count_object,
    create_social_media,
    delete_followed_by,
    delete_user_by_id,
    find_object_by_filter_and_paginate,
    update_followed_by,
    update_social_account,
    update_status_account,
)

client = get_collection_client("social_media")

router = APIRouter()


@router.post("/")
async def add_social(
    body: CreateSocialModel,
):
    social_dict = body.dict()
    existing_user = await client.find_one(
        {
            "$and": [
                {"account_link": social_dict["account_link"]},
                {"social_media": social_dict["social_media"]},
                {"social_type": social_dict["social_type"]},
            ]
        }
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exist"
        )
    await create_social_media(social_dict)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Social media account created successfully."},
    )


@router.get("/social_media/{social_media}/{social_type}")
async def get_social_by_medias(
    social_media: str = Path(
        "Media", title="Social Media", enum=["Facebook", "Twitter", "Tiktok"]
    ),
    social_type: str = Path(
        "Type", title="Social Type", enum=["Object", "Group", "Fanpage", "All"]
    ),
    social_name: str = "",
    page: int = 0,
    limit: int = 10,
):
    invalid_combinations = {
        "Twitter": ["Group", "Fanpage"],
        "Tiktok": ["Group", "Fanpage"],
    }
    filter_object = {"social_media": social_media}
    if social_type != "All":
        filter_object["social_type"] = social_type
    if social_name:
        filter_object["social_name"] = {"$regex": f"{social_name}", "$options": "i"}
    if (
        social_media in invalid_combinations
        and social_type in invalid_combinations[social_media]
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"{social_media} has no {social_type} type",
        )
    socials = await find_object_by_filter_and_paginate(filter_object, page, limit)
    count = await count_object(filter_object)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"result": socials, "total_record": count},
    )


@router.delete("/delete_social/{id}")
async def delete_user_social_media(id: str):
    deleted_social_media = await delete_user_by_id(id)
    if deleted_social_media:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.delete("/Social/{id}")
async def delete_user(id: str):
    deleted_user = await delete_user_by_id(id)
    if deleted_user:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.get("/{social_type}")
async def get_social_types(
    social_type: Optional[str] = Path(
        ..., title="Social Type", enum=["Object", "Group", "Fanpage"]
    ),
    social_name: str = "",
    page: int = 0,
    limit: int = 10,
):
    filter_object = {"social_type": social_type}
    if social_name:
        filter_object["social_name"] = {"$regex": f"{social_name}", "$options": "i"}
    results = await find_object_by_filter_and_paginate(filter_object, page, limit)
    count = await count_object(filter_object)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": results, "total_result": count}
    )


@router.put("/edit_social")
async def update_social_config(data: UpdateSocial = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_social = await update_social_account(data)
    if updated_social:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Successful edit social config",
        )
    return status.HTTP_403_FORBIDDEN


@router.put("/add_followed_by")
async def update_followed_by_user(
    id_user: str, list_followeds: List[AddFollowed] = Body(...)
):
    id_obj = ObjectId(id_user)
    followeds = []
    for list_followed in list_followeds:
        followed = AddFollowed(
            followed_id=list_followed.followed_id, username=list_followed.username
        )
        followeds.append(followed)
    await update_followed_by(id_obj, followeds)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Successful edit")


@router.put("/delete_followed_by")
async def delete_followed_by_user(
    id_user: str, id_followeds: List[AddFollowed] = Body(...)
):
    id_obj = ObjectId(id_user)
    list_id_new = []
    for id_user in id_followeds:
        list_id_new.append(id_user)
    await delete_followed_by(id_obj, list_id_new)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Successful delete"
    )


@router.put("/edit_status")
async def update_status(id: str, data: UpdateStatus = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_status = await update_status_account(id, data)
    if updated_status:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
