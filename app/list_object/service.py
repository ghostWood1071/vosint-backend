import pydantic
from bson import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

db = get_collection_client("object")

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


async def find_by_id(id: ObjectId, projection=None):
    return await db.find_one(filter={"_id": id}, projection=projection)


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


async def create_object(Object):
    return await db.insert_one(Object)

async def get_all_object(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_object = []
    async for item in db.find(filter).sort("_id").skip(offset).limit(limit):
        item = object_to_json(item)
        list_object.append(item)
    return list_object


async def count_all_object(filter):
    return await db.count_documents(filter)


async def find_by_filter_and_paginate(
    name: str, type: str, skip: int, limit: int, projection=None
):
    query = {"name": {"$regex": name, "$options": "i"}, "type": type}
    if type:
        query["type"] = type
    offset = (skip - 1) * limit if skip > 0 else 0
    list_object = []
    async for item in db.find(filter=query).sort("_id").skip(offset).limit(limit):
        item = object_to_json(item)
        list_object.append(item)
    return list_object


def object_to_json(Object) -> dict:
    Object["_id"] = str(Object["_id"])
    return Object


async def count_object(Type, name):
    query = {"type": Type, "name": {"$regex": name}}
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
        list_object.append(entity(item))
    return list_object


async def update_object(id: str, data: dict):
    object = await db.find_one({"_id": ObjectId(id)})
    if object:
        updated_object = await db.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_object:
            return status.HTTP_200_OK
        return False


async def delete_object(id: str):
    object_deleted = await db.find_one({"_id": ObjectId(id)})
    if object_deleted:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK


def entity(object):
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
