import datetime
import json
from typing import *
from bson.objectid import ObjectId

from db.init_db import get_collection_client

from .utils import news_to_json
from vosint_ingestion.models import MongoRepository
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import (
    My_ElasticSearch,
)
from elasticsearch import helpers

client = get_collection_client("News")


async def find_news_by_filter(filter, projection=None):
    news = []
    async for new in client.find(filter, projection).sort("_id"):
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
        if "is_read" not in new:
            await client.aggregate([{"$addFields": {"is_read": False}}]).to_list(
                length=None
            )

        if "list_user_read" not in new:
            await client.aggregate([{"$addFields": {"list_user_read": []}}]).to_list(
                length=None
            )

        if "event_list" not in new:
            await client.aggregate([{"$addFields": {"event_list": []}}]).to_list(
                length=None
            )
        news.append(new)
    return news


async def count_news(filter_news):
    return await client.count_documents(filter_news)


async def find_news_by_id(news_id: ObjectId, projection):
    projection["pub_date"] = str(projection["pub_date"])
    return await client.find_one({"_id": news_id}, projection)


async def read_by_id(new_id: str, user_id: str):
    return await client.update_many(
        {"_id": ObjectId(new_id)},
        {"$set": {"is_read": True}, "$addToSet": {"list_user_read": user_id}},
    )


async def unread_by_id(new_id: str, user_id: str):
    news = await client.find().to_list(length=None)
    for item in news:
        if "list_user_read" in item:
            return await client.update_many(
                {"_id": ObjectId(new_id)},
                {
                    "$set": {"is_read": False},
                    "$pull": {"list_user_read": {"$in": [user_id]}},
                },
            )

        if item["list_user_read"] == [] or item["list_user_read"] not in news:
            await client.update_many(
                {"_id": ObjectId(new_id)}, {"$set": {"is_read": False}}
            )


async def find_news_by_ids(ids: List[str], projection: Dict["str", Any]):
    list_ids = []
    for index in ids:
        list_ids.append(ObjectId(index))
    news_list = []
    async for news in client.find({"_id": {"$in": list_ids}}, projection):
        news_list.append(news)
    return news_list


def add_keywords_to_elasticsearch(index, keywords, doc_ids):
    es = My_ElasticSearch()
    actions = []
    for document_id in doc_ids:
        update_action = {
            "_op_type": "update",
            "_index": index,
            "_id": document_id,
            "script": {
                "source": """
                if (ctx._source.{keywords} == null) {{
                    ctx._source.{keywords} = [];
                }}
                ctx._source.{keywords}.addAll(params.values_to_add);
            """,
                "params": {"values_to_add": keywords},
            },
        }
    actions.append(update_action)
    ressult = helpers.bulk(es.es, actions)
    print(ressult)


def get_check_news_contain_list(news_ids, keywords):
    object_filter = [ObjectId(object_id) for object_id in news_ids]
    news, _ = MongoRepository().get_many("News", {"_id": {"$in": object_filter}})
    for item in news:
        item["is_contain"] = False
        item["_id"] = str(item["_id"])
        item["pub_date"] = str(item["pub_date"])
        for keyword in keywords:
            if (
                keyword.lower() in item["title"].lower()
                or keyword.lower() in item["data:content"].lower()
                or keyword.lower() in item["keywords"]
            ):
                item["is_contain"] = True
                break
    return news


def check_news_contain(object_ids: List[str], news_ids: List[str]):
    object_filter = [ObjectId(object_id) for object_id in object_ids]
    objects, _ = MongoRepository().get_many("object", {"_id": {"$in": object_filter}})
    keywords = {}
    for object in objects:
        if object.get("keywords"):
            keywords[str(object["_id"])] = []
            for keyword in list(object["keywords"].values()):
                item_key_words = [key.strip() for key in keyword.split(",")]
                while "" in keywords:
                    keywords.remove("")
                keywords[str(object["_id"])].extend(item_key_words)
    result = get_check_news_contain_list(news_ids, keywords)
    return result
