from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

db = get_collection_client("Source")


async def create_source_group(source):
    return await db.insert_one(source)


async def get(list):
    list_source = []
    async for item in db.find(list).sort("_id"):
        item = source_to_json(item)
        list_source.append(item)
    return list_source


async def find_by_filter_and_paginate(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_source = []
    async for item in db.find(filter).sort("_id").skip(offset).limit(limit):
        item = source_to_json(item)
        list_source.append(item)
    return list_source


def source_to_json(source) -> dict:
    source["_id"] = str(source["_id"])
    return source


async def count_source(filter):
    return await db.count_documents(filter)


async def search_by_filter_and_paginate(name, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_source_group = []
    async for item in db.find(
        {"$or": [{"source_name": {"$regex": name, "$options": "i"}}]}
    ).sort("_id").skip(offset).limit(limit):
        item = source_group_to_json(item)
        list_source_group.append(item)
    return list_source_group


def source_group_to_json(source_group) -> dict:
    source_group["_id"] = str(source_group["_id"])
    return source_group


async def count_search_source_group(name):
    filter = {"source_name": {"$regex": name, "$options": "i"}}
    return await db.count_documents(filter)


async def add_list_infor(source_name: str, id_infor: List[ObjectId]):
    return await db.update_one(
        {"source_name": source_name}, {"$push": {"news": {"$each": id_infor}}}
    )


async def delete_list_infor(id: str, source):
    group = await db.find_one({"_id": ObjectId(id)})
    if group:
        return await db.update_one(group, {"$pull": {"news": {"name": source}}})


async def delete_source_group(id: str):
    group = await db.find_one({"_id": ObjectId(id)})
    if group:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK


async def update_news(id_group: str, source):
    group = await db.find_one({"_id": ObjectId(id_group)})
    if group:
        return await db.update_one(group, {"$push": {"news": source}})


async def update_source_group(id: str, data: dict, list_source):
    source_group = await db.find_one({"_id": ObjectId(id)})

    for item in list_source:
        if data["source_name"] == source_group["source_name"]:
            updated_source_group = await db.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_source_group:
                return {"message": "updated successful"}
            return False

        if data["source_name"] != item["source_name"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="source group not found"
            )


async def hide_show(id: str, run):
    run = await db.find_one({"_id": ObjectId(id)})
    if run["is_hide"] == True:
        return await db.update_one({"_id": ObjectId(id)}, {"$set": {"is_hide": False}})
    elif run["is_hide"] == False:
        return await db.update_one({"_id": ObjectId(id)}, {"$set": {"is_hide": True}})


def entity(source) -> dict:
    infor_list = []

    infor_list.append(entity_source(source))
    return {
        "_id": str(source["_id"]),
        "user_id": source["user_id"],
        "source_name": source["source_name"],
        "news": infor_list,
    }


def entity_source(infor) -> dict:
    return {
        "_id": str(infor["_id"]),
        "name": infor["name"],
        "host_name": infor["host_name"],
        "language": infor["language"],
        "publishing_country": infor["publishing_country"],
        "source_type": infor["source_type"],
    }
