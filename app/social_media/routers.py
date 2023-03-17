from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, status
from fastapi.responses import JSONResponse

from db.init_db import get_collection_client

from .models import CreateSocialModel, UpdateSocial, UpdateStatus
from .services import (
    count_object,
    create_social_media,
    delete_user_by_id,
    find_object_by_filter,
    find_object_by_filter_and_paginate,
    update_social_account,
    update_status_account,
)

client = get_collection_client("socials")

router = APIRouter()


@router.post("/")
async def add_social(
    body: CreateSocialModel,
):
    social_dict = body.dict()
    existing_user = await client.find_one({"social_name": social_dict["social_name"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exist"
        )
    await create_social_media(social_dict)
    return HTTPException(status_code=status.HTTP_200_OK)


@router.get("/social_media/{social_media}/{social_type}")
async def get_social_by_medias(
    social_media: str = Path(
        "Media", title="Social Media", enum=["Facebook", "Twitter", "Tiktok"]
    ),
    social_type: str = Path(
        "Type", title="Social Type", enum=["Object", "Group", "Fanpage"]
    ),
    social_name: str = "",
    page: int = 0,
    limit: int = 10,
):
    INVALID_COMBINATIONS = {
        "Twitter": ["Group", "Fanpage"],
        "Tiktok": ["Group", "Fanpage"],
    }
    filter_object = {"social_media": social_media}
    if social_type:
        filter_object["social_type"] = social_type
    if (
        social_media in INVALID_COMBINATIONS
        and social_type in INVALID_COMBINATIONS[social_media]
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"{social_media} has no {social_type} type",
        )
    if social_name:
        filter_object["social_name"] = {"$regex": f"{social_name}", "$options": "i"}
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
async def update_social(data: UpdateSocial = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_social = await update_social_account(data)
    if updated_social:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.put("/edit_status")
async def update_status(data: UpdateStatus = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_status = await update_status_account(data)
    if updated_status:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
