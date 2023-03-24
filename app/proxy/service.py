from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

proxy_collect = get_collection_client("proxy")


async def create_proxy(proxy):
    created = await proxy_collect.insert_one(proxy)
    new = await proxy_collect.find_one({"id": created.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_proxy():
    list_proxy = []
    async for item in proxy_collect.find():
        list_proxy.append(Entity(item))
    return list_proxy


async def find_by_filter_and_paginate(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_proxy = []
    async for item in proxy_collect.find(filter).sort("_id").skip(offset).limit(limit):
        item = proxy_to_json(item)
        list_proxy.append(item)
    return list_proxy


def proxy_to_json(proxy) -> dict:
    proxy["_id"] = str(proxy["_id"])
    return proxy


async def count_proxy(filter):
    return await proxy_collect.count_documents(filter)


async def search_by_filter_and_paginate(char_name, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_proxy = []
    async for item in proxy_collect.find(
        {"$or": 
            [
                {"name": {"$regex": f".*{char_name}.*", "$options": "i"}}, 
                {"ip_address": {"$regex": f".*{char_name}.*", "$options": "i"}}
            ]
        }
    ).sort("_id").skip(offset).limit(limit):
        item = Proxy_to_json(item)
        list_proxy.append(item)
    return list_proxy


def Proxy_to_json(proxy) -> dict:
    proxy["_id"] = str(proxy["_id"])
    return proxy


async def count_search_proxy(char_name: str):
    filter = {"$or": 
                [
                    {"name": {"$regex": f".*{char_name}.*", "$options": "i"}}, 
                    {"ip_address": {"$regex": f".*{char_name}.*", "$options": "i"}}
                ]
            }
    return await proxy_collect.count_documents(filter)


async def search_proxy(key: str) -> dict:
    list_proxy = []
    async for item in proxy_collect.find(
        {"$or": [{"name": {"$regex": key}}, {"ip_address": {"$regex": key}}]}
    ):
        list_proxy.append(Entity(item))
    return list_proxy


async def update_proxy(id: str, data: dict):
    proxy = await proxy_collect.find_one({"_id": ObjectId(id)})
    if proxy["ip_address"] == data["ip_address"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="proxy ip already exist"
        )
    updated_proxy = await proxy_collect.update_one(
        {"_id": ObjectId(id)}, {"$set": data}
    )
    if updated_proxy:
        return status.HTTP_200_OK
    return False

async def get_proxy_by_id(id) -> dict:
    proxy = await proxy_collect.find_one({"_id": ObjectId(id)})
    if proxy:
        return Entity(proxy)

async def delete_proxy(id: str):
    proxy = await proxy_collect.find_one({"_id": ObjectId(id)})
    if proxy:
        await proxy_collect.delete_one({"_id": ObjectId(id)})
        return True


def Entity(proxy) -> dict:
    return {
        "_id": str(proxy["_id"]),
        "name": proxy["name"],
        "ip_address": proxy["ip_address"],
        "port": proxy["port"],
        "note": proxy["note"],
    }
