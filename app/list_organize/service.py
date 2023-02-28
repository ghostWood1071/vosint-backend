from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

db = get_collection_client("organize")


async def create_organize(organize):
    created_organize = await db.insert_one(organize)
    new = await db.find_one({"id": created_organize.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_organize():
    organizes = []
    async for organ in db.find():
        organizes.append(Entity(organ))
    return organizes


async def get_one_organize(name: str) -> dict:
    list_organize = []
    async for item in db.find({
        "$or": [
            {"name": {"$regex": name}},
        ]
    }):
        list_organize.append(Entity(item))
    return list_organize


async def update_organize(id: str, data: dict):
    organize = await db.find_one({"_id": ObjectId(id)})
    if organize:
        updated_organize = await db.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_organize:
            return status.HTTP_200_OK
        return False


async def delete_organize(id: str):
    organize = await db.find_one({"_id": ObjectId(id)})
    if organize:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK


def Entity(organize) -> dict:
    return {
        "_id": str(organize["_id"]),
        "name": organize["name"],
        "facebook_link": organize["facebook_link"],
        "twitter_link": organize["twitter_link"],
        "profile_link": organize["profile_link"],
        "avatar_url": organize["avatar_url"],
        "profile": organize["profile"],
        "keywords": organize["keywords"],
        "status": organize["status"],
    }
