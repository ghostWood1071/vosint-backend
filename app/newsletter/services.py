from bson.objectid import ObjectId
from .utils import newsletter_to_json
from db.init_db import get_collection_client

client = get_collection_client("newsletter")


async def find_newsletter_by_id(newsletter_id: ObjectId):
    return await client.find_one({"_id": newsletter_id})


async def find_newsletters_by_user_id(user_id: str, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    newsletters = []
    async for newsletter in client.find({
            "user_id": ObjectId(user_id)
    }).sort("_id").skip(offset).limit(limit):
        newsletters.append(newsletter_to_json(newsletter))

    return newsletters


async def create_newsletter(newsletter):
    return await client.insert_one(newsletter)


async def delete_newsletter(newsletter_id):
    return await client.delete_one({"_id": newsletter_id})


async def update_newsletter(newsletter_id: ObjectId, newsletter):
    return await client.update_one({"_id": newsletter_id},
                                   {"$set": newsletter})
