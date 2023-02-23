from typing import List

from bson.objectid import ObjectId

from db.init_db import get_collection_client

from .utils import news_to_json

client = get_collection_client("users")


async def create_user(user):
    created_user = await client.insert_one(user)
    return await client.find_one({"id": created_user.inserted_id})


async def read_user_by_username(username: str):
    return await client.find_one({"username": username})


async def update_user(user_id: ObjectId, user):
    return await client.update_one({"_id": user_id}, {"$set": user})


async def get_all_user():
    users = []
    async for user in client.find():
        users.append(user_entity(user))
    return users


async def get_user(id: str) -> dict:
    users = await client.find_one({"_id": ObjectId(id)})
    if users:
        return user_entity(users)


async def update_bookmark_user(id: ObjectId, datas: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$push": {"bookmark_list": {"$each": datas}}}
    )


async def delete_bookmark_user(id: ObjectId, id_bookmarks: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$pull": {"bookmark_list": {"$in": id_bookmarks}}}
    )


async def update_vital_user(id: ObjectId, vitals: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$push": {"vital_list": {"$each": vitals}}}
    )


async def delete_vital_user(id: ObjectId, id_vitals: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$pull": {"vital_list": {"$in": id_vitals}}}
    )


async def delete_user(id: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True

async def get_vital_ids(id: ObjectId):
    user = await client.find_one({"_id": ObjectId(id)})
    vital_ids = [str(vital_id) for vital_id in user["vital_list"]]
    return vital_ids


def user_entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
        "vital_list": user["vital_list"]
    }

def news_to_json(user) -> dict:
    user["_id"] = str(user["_id"])
    return user
