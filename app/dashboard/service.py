from datetime import datetime, timedelta
from typing import List
from bson.objectid import ObjectId

from db.init_db import get_collection_client
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import (
    My_ElasticSearch,
)

dashboard_client = get_collection_client("dashboard")
object_client = get_collection_client("object")
news_client = get_collection_client("News")
users_client = get_collection_client("users")
client_events = get_collection_client("events")


my_es = My_ElasticSearch()


def convert_to_query(string: List[str]) -> str:
    query = ""
    for idx, s in enumerate(string):
        if s != "":
            if idx >= 1:
                query += " OR "
            query += f'"{s}"'
    return query


async def count_news_country_today():
    cursor = object_client.find({"object_type": "Quốc gia"})
    count = 0
    query = ""
    async for document in cursor:
        count += 1
        keywords = document["keywords"]
        vi = convert_to_query(keywords["vi"].split(","))
        en = convert_to_query(keywords["en"].split(","))
        ru = convert_to_query(keywords["ru"].split(","))
        cn = convert_to_query(keywords["cn"].split(","))

        if vi != "":
            query += f"{vi} OR "
        if en != "":
            query += f"{en} OR "
        if ru != "":
            query += f"{ru} OR "
        if cn != "":
            query += f"{cn} OR "
    queries = query.split(" OR ")
    if queries[-1] == "":
        queries.pop()
    queries[-1] = queries[-1].rstrip(" OR")
    new_query = " OR ".join(queries)

    date = datetime.now().strptime("%Y-%m-%d")
    gte = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    lte = datetime.now().strftime("%Y-%m-%dT00:00:00Z")

    pipeline_dtos = my_es.search_main(
        index_name="vosint",
        query=new_query,
        gte=gte,
        lte=lte,
    )

    if await dashboard_client.find_one({"date": date, "type": "day"}):
        await dashboard_client.update_one(
            {"date": date}, {"$set": {"value": pipeline_dtos.__len__()}}
        )
    else:
        await dashboard_client.insert_one(
            {
                "value": pipeline_dtos.__len__(),
                "date": date,
                "type": "day",
            }
        )


async def count_news_hours():
    print("Here???")
    date_lt = datetime.now().replace(minute=0, second=0, microsecond=0)
    date_gte = date_lt - timedelta(hours=1)
    # convert YYYY-MM-DD HH:mm:ss to YYYY/MM/DD HH:mm:ss
    news_count = await news_client.count_documents(
        {
            "created_at": {
                "$gte": date_gte.strftime("%Y/%m/%d %H:%M:%S"),
                "$lte": date_lt.strftime("%Y/%m/%d %H:%M:%S"),
            }
        }
    )

    if await dashboard_client.find_one(
        {
            "date": date_lt,
            "type": "hour",
        }
    ):
        await dashboard_client.update_one(
            {"date": date_lt}, {"$set": {"value": news_count}}
        )
    else:
        await dashboard_client.insert_one(
            {
                "value": news_count,
                "date": date_lt,
                "type": "hour",
            }
        )


async def news_country_today(start_day: int):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    back_day = today - timedelta(days=start_day)

    dashboard = dashboard_client.find(
        {"date": {"$gte": back_day, "$lte": today}, "type": "day"}
    )

    result = []
    async for document in dashboard:
        result.append(document)

    return result


async def news_hours_today():
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day.replace(hour=23, minute=0, second=0, microsecond=0)

    dashboard = dashboard_client.find(
        {"date": {"$gte": start_of_day, "$lte": end_of_day}, "type": "hour"}
    )

    result = []
    async for document in dashboard:
        result.append(document)

    return result


# New
# Get total of news in seven days
async def news_seven_nearest():
    day_space = 7

    now = datetime.now()
    now = now.today() - timedelta(days=day_space)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        {
            "$group": {
                "_id": {"$substr": ["$created_at", 0, 10]},
                "value": {"$sum": 1},
            }
        },
        {"$sort": {"_id": -1}},
        {"$limit": 7},
    ]

    data = news_client.aggregate(pipeline)

    result = []
    async for document in data:
        result.append(document)

    return result


# Get total of news in seven days by topics (top 5)
async def top_news_by_topic():
    day_space = 7

    now = datetime.now()
    now = now.today() - timedelta(days=day_space)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        {"$unwind": {"path": "$data:class_chude"}},
        {
            "$group": {
                "_id": "$data:class_chude",
                "value": {"$sum": 1},
            }
        },
        {"$sort": {"value": -1}},
        {"$limit": 5},
    ]

    data = news_client.aggregate(pipeline)

    result = []
    async for document in data:
        result.append(document)

    return result


# Get total of news in seven days by countries (top 5)
async def top_news_by_country():
    day_space = 7

    now = datetime.now()
    now = now.today() - timedelta(days=day_space)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        {
            "$group": {
                "_id": "$source_publishing_country",
                "value": {"$sum": 1},
            }
        },
        {"$sort": {"value": -1}},
        {"$limit": 5},
    ]

    data = news_client.aggregate(pipeline)

    result = []
    async for document in data:
        result.append(document)

    return result


# Get total of users
async def total_users():
    data = users_client.find()

    result = []
    async for document in data:
        result.append(document)

    return {"total": len(result)}


# Get total of news in seven days by countries (top 5)
async def top_user_read():
    now = datetime.now()
    start_of_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=28) + timedelta(days=4)
    end_of_day = (next_month - timedelta(days=next_month.day)).replace(
        hour=23, minute=59, second=59
    )

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    print(start_of_day, end_of_day)

    pipeline = [
        # Where
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        # Flatten
        {"$unwind": {"path": "$list_user_read"}},
        # Group with user is key
        {
            "$group": {
                "_id": {"$toObjectId": "$list_user_read"},
                "value": {"$sum": 1},
            }
        },
        # Join with users collection
        {
            "$lookup": {
                "from": "users",
                "let": {"id": "$_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$id"]}}},
                    {
                        "$project": {
                            "hashed_password": 0,
                            "news_bookmarks": 0,
                            "vital_list": 0,
                        }
                    },
                ],
                "as": "user",
            }
        },
        {"$sort": {"value": -1}},
        {"$limit": 5},
    ]

    data = news_client.aggregate(pipeline)

    result = []
    async for document in data:
        result.append(document)

    return result


async def hot_events_today():
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1, seconds=-1)

    pipeline = [
        {
            "$match": {
                "date_created": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        {
            "$project": {
                "new_list_length": {"$size": "$new_list"},
                "event_name": 1,
                "sentiment": 1,
                "date_created": 1,
            }
        },
        {"$sort": {"new_list_length": -1}},
        {"$limit": 10},
    ]
    result = await client_events.aggregate(pipeline).to_list(None)
    return result
