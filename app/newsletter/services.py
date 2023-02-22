from typing import List

from bson.objectid import ObjectId

from db.init_db import get_collection_client

from .models import Tag
from .utils import newsletter_to_json

client = get_collection_client("newsletter")


async def find_newsletter_by_id(newsletter_id: ObjectId):
    return await client.find_one({"_id": newsletter_id})


async def find_newsletters_and_filter(filter_newsletters: dict):
    topics = {"gio_tin": [], "linh_vuc": [], "chu_de": []}

    async for topic in client.find(filter_newsletters).sort([("-id", -1)]):
        topic = newsletter_to_json(topic)

        if "news_id" in topic:
            topic.pop("news_id")

        if "tag" not in topic:
            continue

        if topic["tag"] == Tag.gio_tin:
            topics["gio_tin"].append(topic)

        if topic["tag"] == Tag.linh_vuc:
            topics["linh_vuc"].append(topic)

        if topic["tag"] == Tag.chu_de:
            topics["chu_de"].append(topic)

    return topics


async def create_newsletter(newsletter):
    return await client.insert_one(newsletter)


async def create_news_ids_to_newsletter(
    newsletter_id: ObjectId, news_ids: List[ObjectId]
):
    return await client.update_one(
        {"_id": newsletter_id}, {"$push": {"news_id": {"$each": news_ids}}}
    )


async def delete_newsletter(newsletter_id):
    return await client.delete_one({"_id": newsletter_id})


async def update_newsletter(newsletter_id: ObjectId, newsletter):
    return await client.update_one({"_id": newsletter_id}, {"$set": newsletter})


async def delete_news_ids_in_newsletter(
    newsletter_id: ObjectId, news_ids: List[ObjectId]
):
    return await client.update_one(
        {"_id": newsletter_id}, {"$pull": {"news_id": {"$in": news_ids}}}
    )
