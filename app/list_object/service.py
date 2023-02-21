from bson.objectid import ObjectId
from fastapi import HTTPException, status
from db.init_db import get_collection_client

db = get_collection_client("object")

async def create_object(object):
    created_object = await db.insert_one(object)
    new = await db.find_one({"id": created_object.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail='OK')

async def get_all_object():
    countries = []
    async for organ in db.find():
        countries.append(Entity(organ))
    return countries

async def get_one_object(id: str) -> dict:
    object = await db.find_one({"_id": ObjectId(id)})
    if object: 
        return Entity(object)
    
async def update_object(id: str, data: dict):
    object = await db.find_one({"_id": ObjectId(id)})
    if object:
        updated_object = await db.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
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
        "object_name": object["object_name"],
        "facebook_link": object["facebook_link"],
        "twitter_link": object["twitter_link"],
        "profile_link": object["profile_link"],
        "avatar_url": object["avatar_url"],
        "profile": object["profile"],
        "keywords": object["keywords"],
        "status": object["status"]
    }