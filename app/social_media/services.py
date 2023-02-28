from bson import ObjectId
from fastapi import status

from db.init_db import get_collection_client

client = get_collection_client("social_media")


async def create_user(user):
    created_user = await client.insert_one(user)
    return await client.find_one({"id": created_user.inserted_id})


async def get_social_by_media(social_media: str, page: int = 1, limit: int = 10):
    media_list = (
        await client.find({"social_media": social_media})
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(length=limit)
    )
    return [social_entity(media) for media in media_list]
    # if media:
    #     return social_entity(media)


async def get_social_name(social_name: str) -> dict:
    name_list = []
    async for item in client.find(
        {
            "social_name": {"$regex": social_name},
        }
    ):
        name_list.append(social_entity(item))
    return name_list
    # name_list = await client.find({"social_name": {"$regex": social_name}})
    # if name_list:
    #     return social_entity(name_list)


async def get_social_facebook(social_type: str, page: int = 1, limit: int = 10):
    query = {"social_media": "Facebook"}
    if social_type:
        query["social_type"] = social_type
    type_list = (
        await client.find(query)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(length=limit)
    )
    return [social_entity(types) for types in type_list]


async def update_social_account(id: str, data: dict):
    socials = await client.find_one({"_id": ObjectId(id)})
    if socials:
        updated_social = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_social:
            return status.HTTP_200_OK
        return False


async def update_status_account(id: str, data: dict):
    socials = await client.find_one({"_id": ObjectId(id)})
    if socials:
        updated_status = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_status:
            return status.HTTP_200_OK
        return False


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
