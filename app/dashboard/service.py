from datetime import datetime, timedelta
from typing import List
from bson import ObjectId

from db.init_db import get_collection_client
from vosint_ingestion.features.pipeline.services import PipelineService
from vosint_ingestion.features.job import get_news_from_newsletter_id__
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import (
    My_ElasticSearch,
)
import json
import os

dashboard_client = get_collection_client("dashboard")
object_client = get_collection_client("object")
news_client = get_collection_client("News")
users_client = get_collection_client("users")
events_client = get_collection_client("events")
event_client = get_collection_client("event")
his_log_client = get_collection_client("his_log")
pipelines_client = get_collection_client("pipelines")
newsletter_client = get_collection_client("newsletter")
report_client = get_collection_client("report")


my_es = My_ElasticSearch()

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


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
    date_lt = datetime.now().replace(minute=0, second=0, microsecond=0)
    date_gte = date_lt - timedelta(hours=1)
    """convert YYYY-MM-DD HH:mm:ss to YYYY/MM/DD HH:mm:ss"""
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


""" START LEADER """


async def news_seven_nearest(day_space: int = 7):
    """Get total of news in seven days"""
    now = datetime.now()
    now = now.today() - timedelta(days=day_space - 1)
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


"""
async def top_news_by_topic(day_space=7):
    #Get total of news in seven days by topics (top 5) with key: data:class_linhvuc
    now = datetime.now()
    now = now.today() - timedelta(days=day_space - 1)
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
        {"$unwind": {"path": "$data:class_linhvuc"}},
        {
            "$group": {
                "_id": "$data:class_linhvuc",
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
"""


async def top_news_by_topic(day_space=7):
    # Get total of news in seven days by topics (top 5) with key: data:class_linhvuc
    now = datetime.now()
    now = now.today() - timedelta(days=day_space - 1)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    start_of_day = start_of_day.strftime("%d/%m/%Y")
    end_of_day = end_of_day.strftime("%d/%m/%Y")

    data_fields = await newsletter_client.find(
        {"tag": "linh_vuc"}, {"_id": 1, "title": 1}
    ).to_list(None)

    result = []

    for field in data_fields:
        data_es = None
        try:
            data_es = get_news_from_newsletter_id__(
                news_letter_id=field["_id"],
                page_size=10000,
                start_date=start_of_day,
                end_date=end_of_day,
            )
        except:
            pass

        if data_es:
            result.append({"_id": field["title"], "value": len(data_es)})

    if len(result) > 0:
        result = sorted(result, key=lambda x: x["value"], reverse=True)

    result = result[0:5]

    return result


async def top_news_by_country(day_space: int = 7, top: int = 5):
    """Get total of news in seven days by countries (top 5)"""
    now = datetime.now()
    now = now.today() - timedelta(days=day_space - 1)
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
        {"$limit": top},
    ]

    data = news_client.aggregate(pipeline)

    result = []
    async for document in data:
        result.append(document)

    return result


async def top_country_by_entities(
    day_space: int = 7, top: int = 5, start_date=None, end_date=None
):
    """Get countries and total of events in seven days by entities (top 5)"""
    now = datetime.now()
    now = now.today() - timedelta(days=day_space - 1)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    # start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    # end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    # filter by start_date, end_date, text_search
    if start_date:
        start_of_day = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_of_day = end_date.replace(hour=23, minute=59, second=59)

    f = open(os.path.join(__location__, "data_static/countries.json"), "r")

    dataJ = json.loads(f.read())

    countries = []
    if dataJ:
        for i in dataJ:
            countries.append(i["name"])

    f.close()

    pipeline = [
        {"$unionWith": {"coll": "event"}},
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
                "_id": 1,
                "list_KT": {"$split": ["$khach_the", ", "]},
                "list_CT": {"$split": ["$chu_the", ", "]},
            },
        },
        {
            "$project": {
                "_id": 1,
                "list_entities": {"$concatArrays": ["$list_KT", "$list_CT"]},
            }
        },
        {
            "$unwind": {
                "path": "$list_entities",
            }
        },
        {"$match": {"list_entities": {"$in": countries}}},
        {"$group": {"_id": "$list_entities", "value": {"$sum": 1}}},
        {"$project": {"country": "$_id", "value": 1}},
        {"$sort": {"value": -1}},
        {"$limit": top},
    ]

    data = events_client.aggregate(pipeline)

    result = []
    async for document in data:
        result.append(document)

    return result


async def total_users():
    """Get total of users"""
    data = users_client.find()

    result = []
    async for document in data:
        result.append(document)

    return {"total": len(result)}


"""Get top users in one month"""
"""
async def top_user_read():
    now = datetime.now()
    start_of_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=28) + timedelta(days=4)
    end_of_day = (next_month - timedelta(days=next_month.day)).replace(
        hour=23, minute=59, second=59
    )

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        Where
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        Flatten
        {"$unwind": {"path": "$list_user_read"}},
        Group with user is key
        {
            "$group": {
                "_id": {"$toObjectId": "$list_user_read"},
                "value": {"$sum": 1},
            }
        },
        Join with users collection
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
"""


async def top_user_read(limit=5):
    """Get users created most reports"""
    now = datetime.now()
    start_of_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=28) + timedelta(days=4)
    end_of_day = (next_month - timedelta(days=next_month.day)).replace(
        hour=23, minute=59, second=59
    )

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "user_id": {"$ne": None},
                # "created_at": {
                #     "$gte": start_of_day,
                #     "$lte": end_of_day,
                # },
            },
        },
        {
            "$unwind": {
                "path": "$headings",
            },
        },
        {
            "$unwind": {
                "path": "$headings.eventIds",
            },
        },
        {
            "$group": {
                "_id": "$user_id",
                "headings": {"$push": "$headings"},
            },
        },
        {
            "$addFields": {
                "total": {"$size": "$headings"},
            },
        },
        {
            "$lookup": {
                "from": "users",
                "let": {"id": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$eq": ["$_id", {"$toObjectId": "$$id"}]},
                        },
                    },
                    {
                        "$project": {
                            "hashed_password": 0,
                            "news_bookmarks": 0,
                            "vital_list": 0,
                        },
                    },
                ],
                "as": "users",
            },
        },
        {
            "$project": {
                "_id": 0,
                "user_id": "$_id",
                "total": 1,
                "user": {"$arrayElemAt": ["$users", 0]},
            },
        },
        {
            "$sort": {
                "total": -1,
            },
        },
        {
            "$limit": limit,
        },
    ]

    data = await report_client.aggregate(pipeline).to_list(None)

    return data


async def hot_events_today():
    """Get news of current day"""
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1, seconds=-1)

    pipeline = [
        {
            "$match": {
                "date_created": {
                    "$gte": start_of_day,
                    "$lte": end_of_day,
                },
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
        {"$match": {"new_list_length": {"$ne": 0}}},
        {"$limit": 10},
    ]

    result = await event_client.aggregate(pipeline).to_list(None)

    return result


async def users_online():
    """Get users online"""
    pipeline = [
        {"$match": {"online": True}},
        {"$count": "online"},
        {"$project": {"total": "$online"}},
    ]

    data = await users_client.aggregate(pipeline).to_list(None)

    result = {}
    for i in data:
        result = i

    return result


""" END LEADER """


""" START EXPERT """


async def source_news_lowest_hightest(days: int = 1):
    now = datetime.now()
    end_of_day = now
    start_of_day = end_of_day - timedelta(days=int(days))

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lte": end_of_day,
                }
            }
        },
        {"$group": {"_id": "$source_name", "value": {"$sum": 1}}},
        {"$project": {"source_name": "$_id", "_id": 0, "value": 1}},
        {"$sort": {"value": -1}},
        {
            "$group": {
                "_id": None,
                "highest": {"$first": "$$ROOT"},
                "lowest": {"$last": "$$ROOT"},
            }
        },
        {"$project": {"_id": 0, "highest": 1, "lowest": 1}},
    ]

    result = {}
    data = news_client.aggregate(pipeline)

    async for i in data:
        result = i

    return result


async def total_news_by_time(days: int = 1):
    now = datetime.now()
    end_of_day = now
    start_of_day = end_of_day - timedelta(days=int(days))

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lte": end_of_day,
                }
            }
        },
        {"$count": "source_name"},
        {"$project": {"total": "$source_name"}},
    ]

    result = {}
    data = news_client.aggregate(pipeline)

    async for i in data:
        result = i

    return result


async def news_read_by_user(day_space: int = 7, user_id=""):
    if not user_id:
        return []
    """Get total of news in seven days by countries (top 5)"""

    """Drunk code. Database hasn't time of read news"""
    now = datetime.now()
    now = now.today() - timedelta(days=day_space - 1)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_of_day,
                    "$lte": end_of_day,
                },
                "is_read": True,
                "list_user_read": {"$in": [user_id]},
            }
        },
        {"$count": "is_read"},
        {"$project": {"total": "$is_read"}},
    ]

    result = {}
    data = news_client.aggregate(pipeline)

    async for i in data:
        result = i

    return result


""" END EXPERT """


""" START ADMIN """


# async def status_source_news(day_space: int = 7, start_date=None, end_date=None):
#     now = datetime.now()
#     now = now.today() - timedelta(days=day_space)
#     start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

#     start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
#     end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

#     pipelineService = PipelineService()

#     result = {
#         "normal": 0,
#         "error": 0,
#         "unknown": 0,
#     }
#     data = pipelineService.get_pipelines(page_size=10000)

#     if data[0]:
#         for pipeline in data[0]:
#             if pipeline.enabled and pipeline.actived:
#                 id: str = pipeline._id
#                 mini_pipeline = [
#                     {
#                         "$match": {
#                             "created_at": {"$gte": start_of_day, "$lte": end_of_day},
#                             "pipeline_id": id,
#                             "log": "completed",
#                         }
#                     },
#                 ]

#                 dataLogs = await his_log_client.aggregate(mini_pipeline).to_list(None)

#                 if len(dataLogs) > 0:
#                     result["normal"] += 1
#                 else:
#                     result["error"] += 1
#             else:
#                 result["unknown"] += 1

#     return result


async def status_source_news(day_space: int = 7, start_date=None, end_date=None):
    now = datetime.now()
    now = now.today() - timedelta(days=day_space)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    if start_date:
        start_of_day = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_of_day = end_date.replace(hour=23, minute=59, second=59)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    list_hist = await his_log_client.aggregate(
        [
            {
                "$match": {
                    "created_at": {"$gte": start_of_day, "$lte": end_of_day},
                }
            }
        ]
    ).to_list(None)

    list_pipelines = await pipelines_client.aggregate([]).to_list(None)

    result = {
        "normal": 0,
        "error": 0,
        "unknown": 0,
    }

    if list_pipelines:
        for pipeline in list_pipelines:
            if pipeline["enabled"]:
                id = pipeline["_id"]

                is_completed = False
                is_unknown = True
                for his in list_hist:
                    if ObjectId(his["pipeline_id"]) == id:
                        is_unknown = False
                        if his["log"] == "completed":
                            is_completed = True
                            result["normal"] += 1
                            break

                if not is_completed and not is_unknown:
                    result["error"] += 1
                elif is_unknown:
                    result["unknown"] += 1

            else:
                result["unknown"] += 1

    return result


async def status_error_source_news(
    day_space: int = 7, start_date=None, end_date=None, page_index=1, page_size=10
):
    now = datetime.now()
    now = now.today() - timedelta(days=day_space)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    if start_date:
        start_of_day = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_of_day = end_date.replace(hour=23, minute=59, second=59)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    list_hist = await his_log_client.aggregate(
        [
            {
                "$match": {
                    "created_at": {"$gte": start_of_day, "$lte": end_of_day},
                }
            }
        ]
    ).to_list(None)

    list_pipelines = await pipelines_client.aggregate([]).to_list(None)

    result = {
        "normal": 0,
        "error": 0,
        "unknown": 0,
    }
    pipeline_err = {}
    if list_pipelines:
        for pipeline in list_pipelines:
            if pipeline["enabled"]:
                id = pipeline["_id"]

                is_completed = False
                is_unknown = True
                for his in list_hist:
                    if ObjectId(his["pipeline_id"]) == id:
                        is_unknown = False
                        if his["log"] == "completed":
                            is_completed = True
                            result["normal"] += 1
                            break

                if not is_completed and not is_unknown:
                    result["error"] += 1
                    pipeline_err[id] = 1
                elif is_unknown:
                    result["unknown"] += 1

            else:
                result["unknown"] += 1

            pipeline_filter = [pl_id for pl_id in pipeline_err.keys()]
            offset = (page_index - 1) * page_index if page_index > 0 else 0
            err_pipeline_list = []
            async for item in pipelines_client.find(
                {"_id": {"$in": pipeline_filter}}
            ).skip(offset).limit(page_size):
                err_pipeline_list.append(item)
    return {"total": len(pipeline_filter), "data": err_pipeline_list}


""" END ADMIN """
