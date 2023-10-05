import pydantic
from bson import ObjectId, regex
from fastapi import HTTPException, status
from unidecode import unidecode
from vosint_ingestion.models.mongorepository import MongoRepository

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
    name: str, type: str | None, skip: int, limit: int
):
    query = {"name": {"$regex": name, "$options": "i"}, "object_type": type}
    if type:
        query["object_type"] = type
    offset = (skip - 1) * limit if skip > 0 else 0
    list_object = []
    async for item in db.find(query).sort("_id").skip(offset).limit(limit):
        item = object_to_json(item)
        list_object.append(item)
    return list_object


def object_to_json(Object) -> dict:
    Object["_id"] = str(Object["_id"])
    return Object


async def count_object(Type, name):
    query = {"object_type": Type, "name": {"$regex": name}}
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
        item = object_to_json(item)
        list_object.append(item)
    return list_object


async def update_object(id: str, data: dict):
    object = await db.find_one({"_id": ObjectId(id)})

    list_object = await db.find().to_list(length=None)

    for item in list_object:
        if item["_id"] != object["_id"] and item["name"] == data["name"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Object is duplicated"
            )

    # if object["name"] == data["name"]:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exist")

    updated_object = await db.find_one_and_update({"_id": ObjectId(id)}, {"$set": data})
    if updated_object:
        return status.HTTP_200_OK
    else:
        return False


async def delete_object(id: str):
    object_deleted = await db.find_one({"_id": ObjectId(id)})
    if object_deleted:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK


def update_news(object_id: str, my_es):
    try:
        object = MongoRepository().get_one("object", {"_id": object_id})
        if object is None:
            return False
        key_str = ""
        for key in object.get("keywords").keys():
            key_str += object.get("keywords").get(key) + ","
        key_arr = [key.strip() for key in key_str.split(",")]
        key_arr = list(filter(lambda x: x != "", key_arr))
        search_text = " | ".join(key_arr)
        data = my_es.search_main("vosint", query=search_text, size=1000)
        insert_list = [row.get("_id") for row in data]
        MongoRepository().update_many(
            "object",
            {"_id": ObjectId(object_id)},
            {"$addToSet": {"news_list": {"$each": insert_list}}},
        )
        return True
    except Exception as e:
        print(e)
        return False
