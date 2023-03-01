from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse

from app.proxy.model import CreateProxy, UpdateProxy
from app.proxy.service import (
    count_proxy,
    create_proxy,
    delete_proxy,
    find_by_filter_and_paginate,
    get_all_proxy,
    search_proxy,
    update_proxy,
    search_by_filter_and_paginate,
    count_search_proxy
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
async def get_all(skip = 0, limit = 10):
    list_proxy = await find_by_filter_and_paginate({}, int(skip), int(limit))
    count = await count_proxy({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": list_proxy, "total_record": count}
    )

@router.get("/{name}")
async def search(name, skip = 0, limit = 10):
    search_proxy = await search_by_filter_and_paginate(name, int(skip), int(limit))
    count = await count_search_proxy({})
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": search_proxy, "total_record": count}
    )


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
