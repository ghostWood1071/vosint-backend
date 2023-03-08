from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.manage_news.model import (
    CreateSource,
    CreateSourceGroup,
    UpdateSourceGroup,
    UpdateState,
)
from app.manage_news.service import (
    add_list_infor,
    count_search_source_group,
    count_source,
    create_source_group,
    delete_list_infor,
    delete_source_group,
    find_by_filter_and_paginate,
    get_all_source,
    hide_show,
    search_by_filter_and_paginate,
    update_news,
    update_source_group,
)
from db.init_db import get_collection_client

router = APIRouter()

db = get_collection_client("Source")


# @router.post("/")
# async def add_source(payload: CreateSourceGroup):
#     source = payload.dict()
#     exist_source = await db.find_one({"source_name": source["source_name"]})
#     if exist_source:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail="source already exist"
#         )
#     new_source = await create_source_group(source)
#     return new_source

@router.post("/")
async def create(data: SourceGroupSchema= Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    source = data.dict()
    source["user_id"] = user_id
    exist_source = await db.find_one({"source_name": source["source_name"]})
    if exist_source:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="source already exist"
        )
    new_source = await create_source_group(source)
    return new_source


@router.get("/")
async def get_all(skip=0, limit=10):
    list_source_group = await find_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_source({})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": list_source_group, "total_record": count},
    )
    
@router.get("/{name}")
async def search(name, skip = 0, limit = 10):
    search_source_group = await search_by_filter_and_paginate(name, int(skip), int(limit))
    Count = await count_search_source_group({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": search_source_group, "total_record": Count}
    )


@router.post("/add-source/{id}")
async def add_news(id: str, payload: CreateSource = Body(...)):
    Payload = payload.dict()    
    await update_news(id, Payload)
    payload.id_source = ObjectId()
    return status.HTTP_201_CREATED

@router.post("/run-hide-show/{id}")
async def hide_and_show(id: str, payload: UpdateState = Body(...)):
    
    data = payload.dict()
    await hide_show(id, data)
    return 200

# @router.post("/add-source/{name}")
# async def add_infor(name: str, list_id_infor: List[str] = Body(...)):
#     list_infor = []
#     for item in list_id_infor:
#         list_infor.append(ObjectId(item))
#     await add_list_infor(name, list_id_infor)
#     return status.HTTP_201_CREATED


@router.put("/delete-infor/{id}")
async def delete_infor(id: str, list_source: str):
    # list_infor = []
    # for item in list_source:
    #     list_infor.append(item)
    await delete_list_infor(id, list_source)
    return status.HTTP_201_CREATED

@router.put("/update-source-group/{id}")
async def update_all(id: str, data: UpdateSourceGroup = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_source_group = await update_source_group(id, data)
    if updated_source_group:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN

@router.delete("/{id}")
async def delete_source(id):
    Deleted_group_source = await delete_source_group(id)
    if Deleted_group_source:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
