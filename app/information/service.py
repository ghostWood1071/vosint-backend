from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

infor_collect = get_collection_client("infor")


async def create_infor(infor):
    created = await infor_collect.insert_one(infor)
    new = await infor_collect.find_one({"id": created.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_infor():
    list_infor = []
    async for item in infor_collect.find():
        list_infor.append(Entity(item))
    return list_infor


async def find_by_filter_and_paginate(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_infor = []
    async for item in infor_collect.find(filter).sort("_id").skip(offset).limit(limit):
        item = infor_to_json(item)
        list_infor.append(item)
    return list_infor


def infor_to_json(infor) -> dict:
    infor["_id"] = str(infor["_id"])
    return infor


async def count_infor(filter):
    return await infor_collect.count_documents(filter)


async def search_by_filter_and_paginate(name, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_infor = []
    async for item in infor_collect.find(
        {"$or": [{"name": {"$regex": name}}, {"host_name": {"$regex": name}}]}
    ).sort("_id").skip(offset).limit(limit):
        item = Infor_to_json(item)
        list_infor.append(item)
    return list_infor


def Infor_to_json(infor) -> dict:
    infor["_id"] = str(infor["_id"])
    return infor


async def count_search_infor(name: str):
    name_filter = {"name": {"$regex": name}}
    return await infor_collect.count_documents(name_filter)


async def search_infor(keyword: str) -> dict:
    list_infor = []
    async for item in infor_collect.find(
        {"$or": [{"name": {"$regex": keyword}}, {"host_name": {"$regex": keyword}}]}
    ):
        list_infor.append(Entity(item))
    return list_infor


async def update_infor(id: str, data: dict):
    infor = await infor_collect.find_one({"_id": ObjectId(id)})
    if infor:
        updated_infor = await infor_collect.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_infor:
            return status.HTTP_200_OK
        return False


async def delete_infor(id: str):
    infor = await infor_collect.find_one({"_id": ObjectId(id)})
    if infor:
        await infor_collect.delete_one({"_id": ObjectId(id)})
        return True


def Entity(infor) -> dict:
    return {
        "_id": str(infor["_id"]),
        "name": infor["name"],
        "host_name": infor["host_name"],
        "language": infor["language"],
        "publishing_country": infor["publishing_country"],
        "source_type": infor["source_type"],
    }
