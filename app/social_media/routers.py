from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from db.init_db import get_collection_client

from .models import CreateSocialModel, UpdateSocial, UpdateStatus
from .services import (
    create_user,
    get_social_by_media,
    get_social_facebook,
    get_social_name,
    update_social_account,
    update_status_account,
)

client = get_collection_client("socials")

router = APIRouter()


@router.post("/")
async def add_social(
    body: CreateSocialModel,
    _q: str = Query("Social", enum=["Facebook", "Twitter", "Tiktok"]),
    _p: Optional[str] = Query("Type", enum=["Đối tượng", "Nhóm", "Fanpage"]),
):
    social_dict = body.dict()
    existing_user = await client.find_one({"social_name": social_dict["social_name"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exist"
        )
    social_dict["social_media"] = _q
    if _q == "Facebook":
        if not _p:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing social type"
            )
        social_dict["social_type"] = _p
    else:
        social_dict["social_type"] = None
    await create_user(social_dict)
    return HTTPException(status_code=status.HTTP_200_OK)


@router.get("/social_media/{social_media}")
async def get_social_by_medias(
    social_media: str = Path(
        "Media", title="Social Media", enum=["Facebook", "Twitter", "Tiktok"]
    ),
    # social_type: str | None = None,
    page: int = 1,
    limit: int = 10,
):
    # social_media = _p
    if social_media not in ["Facebook", "Twitter", "Tiktok"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid social media"
        )
    socials = await get_social_by_media(social_media, page, limit)
    return socials


@router.get("/social_type/{social_type}")
async def get_social_by_types(
    social_type: str = Path(
        ..., title="Social Type", enum=["Đối tượng", "Nhóm", "Fanpage"]
    ),
    page: int = 1,
    limit: int = 10,
):
    types = await get_social_facebook(social_type, page, limit)
    return types


@router.get("/social_name/{social_name}")
async def get_social_by_name(social_name: str):
    name_list = await get_social_name(social_name)
    if name_list:
        return name_list
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="name not exist")


@router.put("/edit_social/{social_id}")
async def update_social(id: str, data: UpdateSocial = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_social = await update_social_account(id, data)
    if updated_social:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.put("/edit_status/{social_id}")
async def update_status(id: str, data: UpdateStatus = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_status = await update_status_account(id, data)
    if updated_status:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
