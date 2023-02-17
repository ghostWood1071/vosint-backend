from bson.objectid import ObjectId

from db.init_db import get_collection_client

# from fastapi import status


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


# async def update_user(id: str, data: dict):
#     if len(data) < 1:
#         return False
#     user = await client.find_one({"_id": ObjectId(id)})
#     if user:
#         updated_user = await client.update_one({"_id": ObjectId(id)},
#                                                {"$set": data})
#         if updated_user:
#             return status.HTTP_200_OK
#         return False
#


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
    }
