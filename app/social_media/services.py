from bson import ObjectId
from fastapi import status

from app.social_media.utils import object_to_json
from db.init_db import get_collection_client

client = get_collection_client("social_media")


async def create_social_media(user):
    created_user = await client.insert_one(user)
    return await client.find_one({"id": created_user.inserted_id})


async def delete_user_by_id(id: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True


async def update_social_account(data: dict):
    id = data["id"]
    socials = await client.find_one({"_id": ObjectId(id)})
    if socials:
        updated_social = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_social:
            return status.HTTP_200_OK
        return False


async def update_status_account(data: dict):
    id = data["id"]
    socials = await client.find_one({"_id": ObjectId(id)})
    if socials:
        updated_status = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_status:
            return status.HTTP_200_OK
        return False


async def find_object_by_filter_and_paginate(filter_object, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    objects = []
    async for new in client.find(filter_object).sort("_id").skip(offset).limit(limit):
        new = object_to_json(new)
        objects.append(new)

    return objects


async def find_object_by_filter(filter_object):
    objects = []
    async for new in client.find(filter_object).sort("_id"):
        new = object_to_json(new)
        objects.append(new)

    return objects


async def count_object(filter_object):
    return await client.count_documents(filter_object)


def social_entity(socials) -> dict:
    return {
        "_id": str(socials["_id"]),
        "social_name": socials["social_name"],
        "social_media": socials["social_media"],
        "social_type": socials["social_type"],
        "account_link": socials["account_link"],
        "avatar_url": socials["avatar_url"],
        "profile": socials["profile"],
        "is_active": bool(socials["is_active"]),
    }
