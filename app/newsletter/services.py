from typing import List

from bson.objectid import ObjectId

from db.init_db import get_collection_client

from .models import Tags
from .utils import newsletter_to_json

client = get_collection_client("newsletter")


async def find_newsletter_by_id(newsletter_id: ObjectId):
    return await client.find_one({"_id": newsletter_id})


async def find_newsletters_and_filter(filter_newsletters: dict):
    topics = {"newsletters": [], "fields": [], "topics": []}
    async for topic in client.find(filter_newsletters).sort("_id"):
        topic = newsletter_to_json(topic)
        if "news_id" in topic:
            topic.pop("news_id")

        if topic["tags"] == Tags.newsletter:
            topics["newsletters"].append(topic)

        if topic["tags"] == Tags.field:
            topics["fields"].append(topic)

        if topic["tags"] == Tags.topic:
            topics["topics"].append(topic)

    return topics


async def create_newsletter(newsletter):
    return await client.insert_one(newsletter)


async def create_news_ids_to_newsletter(newsletter_id: ObjectId,
                                        news_ids: List[ObjectId]):
    return await client.update_one({"_id": newsletter_id},
                                   {"$push": {
                                       "news_id": {
                                           "$each": news_ids
                                       }
                                   }})


async def delete_newsletter(newsletter_id):
    return await client.delete_one({"_id": newsletter_id})


async def update_newsletter(newsletter_id: ObjectId, newsletter):
    return await client.update_one({"_id": newsletter_id},
                                   {"$set": newsletter})


async def update_newsletter_news_list(newsletter_id: ObjectId,
                                      news_id: ObjectId):
    return await client.update_one({"_id": newsletter_id},
                                   {"$pull": {
                                       "news_id": news_id
                                   }})
