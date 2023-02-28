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


async def add_list_infor(source_name: str, id_infor: List[ObjectId]):
    return await db.update_one(
        {"source_name": source_name}, {"$push": {"news": {"$each": id_infor}}}
    )


async def delete_list_infor(source_name: str, id_infor: List[ObjectId]):
    return await db.update_one(
        {"source_name": source_name}, {"$pull": {"news": {"$in": id_infor}}}
    )


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
