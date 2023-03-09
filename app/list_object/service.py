from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

db = get_collection_client("object")


async def search_by_filter_and_paginate(type, skip: int, limit: int):
    query = {"type": type}
    if type:
        query["type"] = type
    offset = (skip - 1) * limit if skip > 0 else 0
    list_object = []
    async for item in db.find(query).sort("_id").skip(offset).limit(limit):
        item = object_to_json(item)
        list_object.append(item)
    return list_object


async def count_search_object(type: str):
    type_filter = {"name": type}
    return await db.count_documents(type_filter)


async def create_object(object):
    created_object = await db.insert_one(object)
    new = await db.find_one({"id": created_object.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_object(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_Object = []
    async for item in db.find(filter).sort("_id").skip(offset).limit(limit):
        item = object_to_json(item)
        list_Object.append(item)
    return list_Object


async def count_all_object(filter):
    return await db.count_documents(filter)


async def find_by_filter_and_paginate(name: str, type: str, skip: int, limit: int):
    query = {"name": {"$regex": name}, "type": type}
    if type:
        query["type"] = type
    offset = (skip - 1) * limit if skip > 0 else 0
    list_object = []
    async for item in db.find(query).sort("_id").skip(offset).limit(limit):
        item = object_to_json(item)
        list_object.append(item)
    return list_object


def object_to_json(object) -> dict:
    object["_id"] = str(object["_id"])
    return object


async def count_object(type, name):
    print(type)
    query = {"type": type, "name": {"$regex": name}}
    return await db.count_documents(query)


async def get_one_object(name: str) -> dict:
    list_object = []
    async for item in db.find(
        {
            "$or": [
                {"name": {"$regex": name}},
            ]
        }
    ):
        list_object.append(Entity(item))
    return list_object


async def update_object(id: str, data: dict):
    object = await db.find_one({"_id": ObjectId(id)})
    if object:
        updated_object = await db.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_object:
            return status.HTTP_200_OK
        return False


async def delete_object(id: str):
    object = await db.find_one({"_id": ObjectId(id)})
    if object:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK


def Entity(object) -> dict:
    return {
        "_id": str(object["_id"]),
        "name": object["name"],
        "facebook_link": object["facebook_link"],
        "twitter_link": object["twitter_link"],
        "profile_link": object["profile_link"],
        "avatar_url": object["avatar_url"],
        "profile": object["profile"],
        "keywords": object["keywords"],
        "type": object["type"],
        "status": object["status"],
    }
