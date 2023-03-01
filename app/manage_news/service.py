from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

db = get_collection_client("Source")


async def create_source_group(source):
    created_source = await db.insert_one(source)
    new = await db.find_one({"id": created_source.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_source():
    source_group = []
    async for item in db.find():
        source_group.append(Entity(item))
    return source_group

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


async def add_list_infor(source_name: str, id_infor: List[ObjectId]):
    return await db.update_one(
        {"source_name": source_name}, {"$push": {"news": {"$each": id_infor}}}
    )

async def delete_list_infor(source_name: str, id_infor: List[ObjectId]):
    return await db.update_one(
        {"source_name": source_name}, {"$pull": {"news": {"$in": id_infor}}}
    )

async def delete_source_group(id: str):
    group = await db.find_one({"_id": ObjectId(id)})
    if group:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK

# async def update_news(source_name: str, news):
#     return await db.update_one(
#         {"source_name": source_name},
#         {"$push": {"news": news}}
#     )


def Entity(source) -> dict:
    infor_list = []
    if "news" in source:
        for infor_id in source["news"]:
            infor_list.append(str(infor_id))

    return {
        "_id": str(source["_id"]),
        "user_id": source["user_id"],
        "source_name": source["source_name"],
        "news": infor_list,
    }
