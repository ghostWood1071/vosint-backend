from db.init_db import get_collection_client
from bson.objectid import ObjectId
from fastapi import status


client = get_collection_client("users")

async def add_user(data: dict):
    user = await client.insert_one(data)
    new_user = await client.find_one({"_id": user.inserted_id})
    return userEntity(new_user)

async def get_all_user():
    users = []
    async for user in client.find():
        users.append(userEntity(user))
    return users


async def get_user(id: str) -> dict:
    users = await client.find_one({"_id": ObjectId(id)})
    if users:
        return userEntity(users)
    
async def Update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await client.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if updated_user:
            return status.HTTP_200_OK
        return False
    
async def Delete_user(id: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True
    



def userEntity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"],
        "fullname": user["fullname"],
        "account_type": user["account_type"],
    }