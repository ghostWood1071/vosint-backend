from bson.objectid import ObjectId
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from unidecode import unidecode

from app.proxy.model import CreateProxy, UpdateProxy
from app.proxy.service import (
    count_proxy,
    count_search_proxy,
    create_proxy,
    delete_proxy,
    find_by_filter_and_paginate,
    get_all_proxy,
    get_proxy_by_id,
    search_by_filter_and_paginate,
    search_proxy,
    update_proxy,
)
from db.init_db import get_collection_client

router = APIRouter()
proxy_collect = get_collection_client("proxy")


@router.post("/")
async def add_proxy(payload: CreateProxy):
    proxy = payload.dict()
    exist_proxy = await proxy_collect.find_one({"ip_address": proxy["ip_address"]})
    if exist_proxy:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ip address already exist"
        )
    new_proxy = await create_proxy(proxy)
    return new_proxy


@router.get("/")
async def get_all(skip=0, limit=10):
    list_proxy = await find_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_proxy({})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": list_proxy, "total_record": count},
    )


@router.get("/{name}")
async def search(name: str = "", skip=0, limit=10):
    char_name = name
    search_proxy = await search_by_filter_and_paginate(char_name, int(skip), int(limit))
    count = await count_search_proxy(char_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": search_proxy, "total_record": count},
    )
    
@router.get("/one-proxy/{id}")
async def get_id(id: str):
    proxy = await get_proxy_by_id(id)
    if proxy:
        return proxy
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="proxy not exist")

@router.put("/{id}")
async def update(id, data: UpdateProxy = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_proxy = await update_proxy(id, data)
    if updated_proxy:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.delete("/{id}")
async def delete(id):
    deleted_proxy = await delete_proxy(id)
    if deleted_proxy:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
