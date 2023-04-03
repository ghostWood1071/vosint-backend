import datetime
import json

from bson.objectid import ObjectId

from db.init_db import get_collection_client

from .utils import news_to_json

client = get_collection_client("news")


async def find_news_by_filter(filter):
    news = []
    async for new in client.find(filter).sort("_id"):
        new = news_to_json(new)
        news.append(new)

    return news


async def find_news_by_filter_and_paginate(
    filter_news, projection, skip: int, limit: int
):
    offset = (skip - 1) * limit if skip > 0 else 0
    news = []
    async for new in client.find(filter_news, projection).sort("_id").skip(
        offset
    ).limit(limit):
        new = news_to_json(new)
        new["pub_date"] = str(new["pub_date"])
        news.append(new)

    return news


async def count_news(filter_news):
    return await client.count_documents(filter_news)


async def find_news_by_id(news_id: ObjectId, projection):
    projection["pub_date"] = str(projection["pub_date"])
    return await client.find_one({"_id": news_id}, projection)
