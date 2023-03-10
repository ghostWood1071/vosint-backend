from typing import List, Union

from bson import ObjectId
from fastapi import APIRouter, Body, File, HTTPException, Path, UploadFile, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.auth.password import get_password_hash
from app.news.services import count_news, find_news_by_filter_and_paginate
from app.social_media.services import count_object, find_object_by_filter_and_paginate
from db.init_db import get_collection_client

from .models import Role, UserCreateModel, UserUpdateModel
from .services import (
    count_users,
    create_user,
    delete_bookmark_user,
    delete_interested_object,
    delete_user,
    delete_vital_user,
    find_user_by_id,
    get_users,
    update_bookmark_user,
    update_interested_object,
    update_user,
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


@router.get("/vital")
async def get_vital_by_user(skip=0, limit=20, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await find_user_by_id(ObjectId(user_id))
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    if "vital_list" not in user:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )

    news = await find_news_by_filter_and_paginate(
        {"_id": {"$in": user["vital_list"]}}, int(skip), int(limit)
    )

    count = await count_news({"_id": {"$in": user["vital_list"]}})

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": news, "total_record": count}
    )


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


@router.get("/interested")
async def get_interested_objects(skip=0, limit=20, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await find_user_by_id(ObjectId(user_id))

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )
    if "interested_list" not in user:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )
    objects = await find_object_by_filter_and_paginate(
        {"_id": {"$in": user["interested_list"]}}, int(skip), int(limit)
    )

    count = await count_object({"_id": {"$in": user["interested_list"]}})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"result": objects, "total_record": count},
    )


@router.get("/interested/{social_media}/{social_type}")
async def get_interested_by_type(
    social_media: str = Path(
        "Media", title="Social Media", enum=["Facebook", "Twitter", "Tiktok"]
    ),
    social_type: str = Path(
        ...,
        title="Social Type",
        description="Facebook chọn cả 3 trường, Twitter và Tiktok chỉ chọn Object",
        enum=["Object", "Group", "Fanpage"],
    ),
    skip: int = 1,
    limit: int = 20,
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await find_user_by_id(ObjectId(user_id))
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )
    if "interested_list" not in user:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": [], "total_record": 0}
        )
    filter_object = {
        "_id": {"$in": user["interested_list"]},
        "social_media": social_media,
        "social_type": social_type,
    }

    objects = await find_object_by_filter_and_paginate(
        filter_object, int(skip), int(limit)
    )
    count = len(objects)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"result": objects, "total_record": count},
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


@router.post("/vital")
async def add_vital(vitals: List[str] = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    list_vitals_news = []
    for vital in vitals:
        list_vitals_news.append(ObjectId(vital))
    await update_vital_user(user_id, list_vitals_news)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Successful add vital news"
    )


@router.put("/vital")
async def delete_vital(
    id_vitals: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    list_vitals_news = []
    for id_vital in id_vitals:
        list_vitals_news.append(ObjectId(id_vital))
    await delete_vital_user(user_id, list_vitals_news)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Successful delete vital news"
    )


@router.post("/interested")
async def add_interested(
    interesteds: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    list_interested_objects = []
    for interested in interesteds:
        list_interested_objects.append(ObjectId(interested))
    await update_interested_object(user_id, list_interested_objects)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Successful add interested objects"
    )


@router.put("/interested")
async def delete_interested(
    id_interesteds: List[str] = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    list_interested_objects = []
    for id_interested in id_interesteds:
        list_interested_objects.append(ObjectId(id_interested))
    await delete_interested_object(user_id, list_interested_objects)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Successful delete interested objects",
    )


@router.get("/")
async def get_all(
    skip=0,
    limit=20,
    name="",
    role: Union[Role, None] = None,
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()

    query = {
        "$or": [
            {"full_name": {"$regex": f"\\b{name}\\b", "$options": "i"}},
            {"full_name": {"$regex": name, "$options": "i"}},
            {"username": {"$regex": f"\\b{name}\\b", "$options": "i"}},
            {"username": {"$regex": name, "$options": "i"}},
        ]
    }

    if role is not None:
        query["$and"] = [{"role": role}]

    users = await get_users(query, int(skip), int(limit))
    count = await count_users(query)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": users, "total_record": count}
    )


@router.put("/me")
async def update_me(
    user_data: UserUpdateModel = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())

    user_data = {k: v for k, v in user_data.dict().items() if v is not None}
    updated_user = await update_user(user_id, user_data)
    if updated_user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.put("/{id}")
async def update(id: str, user_data: UserUpdateModel = Body(...)):
    user_data = {k: v for k, v in user_data.dict().items() if v is not None}
    updated_user = await update_user(ObjectId(id), user_data)
    if updated_user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.delete("/{id}")
async def delete(id: str):
    deleted = await delete_user(id)
    if deleted is not True:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())

    try:
        content = await file.read()
        with open(f"static/{file.filename}", "wb") as f:
            f.write(content)
    except Exception as error:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There was an error when uploading the file",
        )
    finally:
        await file.close()

    await update_user(user_id, {"avatar_url": f"static/{file.filename}"})
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content=f"static/{file.filename}"
    )
