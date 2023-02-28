from typing import List

from bson import ObjectId

from db.init_db import get_collection_client

client = get_collection_client("socials")


async def get_all_user(skip, limit):
    users = []
    async for user in client.find().limit(limit).skip(limit * skip):
        users.append(user_entity(user))
    return users


async def get_user(id: str) -> dict:
    users = await client.find_one({"_id": ObjectId(id)})
    if users:
        return user_entity(users)


async def create_user(user):
    created_user = await client.insert_one(user)
    return await client.find_one({"id": created_user.inserted_id})


async def delete_user(id: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True


async def update_username_user(id: str, username_new: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.update_one(
            {"_id": ObjectId(id)}, {"$set": {"username": username_new}}
        )
        return True


async def update_follow_user(id: ObjectId, datas: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$push": {"users_follow": {"$each": datas}}}
    )


async def delete_follow_user(id: ObjectId, id_users: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$pull": {"users_follow": {"$in": id_users}}}
    )


def user_entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "social": user["social"],
        "users_follow": user["users_follow"],
    }
