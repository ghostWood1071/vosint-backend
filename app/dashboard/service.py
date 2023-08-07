from datetime import datetime, timedelta
from typing import List

from db.init_db import get_collection_client
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import (
    My_ElasticSearch,
)

dashboard_client = get_collection_client("dashboard")
object_client = get_collection_client("object")
news_client = get_collection_client("News")


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
