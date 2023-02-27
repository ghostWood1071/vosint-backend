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


async def search_proxy(key: str) -> dict:
    proxy = await proxy_collect.find_one({"name": key})
    if proxy:
        return Entity(proxy)


async def update_proxy(id: str, data: dict):
    proxy = await proxy_collect.find_one({"_id": ObjectId(id)})
    if proxy:
        updated_proxy = await proxy_collect.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_proxy:
            return status.HTTP_200_OK
        return False


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
