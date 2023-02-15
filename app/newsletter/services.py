from bson.objectid import ObjectId

from .models import Tags
from .utils import newsletter_to_json
from db.init_db import get_collection_client

client = get_collection_client("newsletter")


async def find_newsletter_by_id(newsletter_id: ObjectId):
    return await client.find_one({"_id": newsletter_id})


async def find_newsletters_and_filter(filter_newsletters: dict):
    topics = {
        "newsletters": [],
        "fields": [],
        "topics": []
    }
    async for topic in client.find(filter_newsletters).sort("_id"):
        topic = newsletter_to_json(topic)
        if topic["tags"] is not None:
            if Tags.newsletter in topic["tags"]:
                topics["newsletters"].append(topic)

            if Tags.field in topic["tags"]:
                topics["fields"].append(topic)

            if Tags.topic in topic["tags"]:
                topics["topics"].append(topic)

    return topics


async def create_newsletter(newsletter):
    return await client.insert_one(newsletter)


async def delete_newsletter(newsletter_id):
    return await client.delete_one({"_id": newsletter_id})


async def update_newsletter(newsletter_id: ObjectId, newsletter):
    return await client.update_one({"_id": newsletter_id},
                                   {"$set": newsletter})
