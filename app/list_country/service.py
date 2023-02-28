from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

db = get_collection_client("country")


async def create_country(country):
    created_country = await db.insert_one(country)
    new = await db.find_one({"id": created_country.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_country():
    countries = []
    async for organ in db.find():
        countries.append(Entity(organ))
    return countries


async def get_one_country(name: str):
    list_country = []
    async for item in db.find(
        {
            "$or": [
                {"name": {"$regex": name}},
            ]
        }
    ):
        list_country.append(Entity(item))
    return list_country


async def update_country(id: str, data: dict):
    country = await db.find_one({"_id": ObjectId(id)})
    if country:
        updated_country = await db.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_country:
            return status.HTTP_200_OK
        return False


async def delete_country(id: str):
    country = await db.find_one({"_id": ObjectId(id)})
    if country:
        await db.delete_one({"_id": ObjectId(id)})
        return status.HTTP_200_OK


def Entity(country) -> dict:
    return {
        "_id": str(country["_id"]),
        "name": country["name"],
        "facebook_link": country["facebook_link"],
        "twitter_link": country["twitter_link"],
        "profile_link": country["profile_link"],
        "avatar_url": country["avatar_url"],
        "profile": country["profile"],
        "keywords": country["keywords"],
        "status": country["status"],
    }
