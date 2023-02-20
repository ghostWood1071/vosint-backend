from db.init_db import get_collection_client

from .utils import news_to_json

client = get_collection_client("news")


async def find_news_by_filter_and_paginate(filter_news: dict, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    news = []
    async for new in client.find(filter_news).sort("_id").skip(offset).limit(limit):
        new = news_to_json(new)
        news.append(new)

    return news


async def count_news(filter_news: dict):
    return await client.count_documents(filter_news)
