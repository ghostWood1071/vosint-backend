from typing import List

from bson.objectid import ObjectId

from app.user.models import BookMarkBase
from db.init_db import get_collection_client

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


async def update_bookmark_user(id: ObjectId,datas:List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$push": {"bookmark_list": { "$each": datas }}}
    )

async def delete_bookmark_user(id: ObjectId,id_bookmarks:List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$pull": {"bookmark_list":{ "$in": id_bookmarks}}}
    )   


async def delete_user(id: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True


def user_entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
        "bookmark_list":user["bookmark_list"]
    }
