from datetime import datetime, time, timedelta
from typing import List

import pydantic
from bson.objectid import ObjectId

from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


report_client = get_collection_client("report")
event_client = get_collection_client("event")
event_system_client = get_collection_client("event_system")
new_client = get_collection_client("News")
newsletter_client = get_collection_client("newsletter")

projection = {
    "_id": True,
    "title": True,
    "parent_id": True,
}

projection_event = {"event_name": True, "new_list": True, "date_created": True}

projection_new = {"_id": True, "data:title": True, "data:url": True, "created_at": True}


async def count(filter):
    return await report_client.count_documents(filter)

async def get_reports(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_report = []
    async for report in report_client.find(filter).sort("_id").skip(offset).limit(
        limit
    ):
        list_report.append(report)

    return list_report

async def find_report_by_filter(filter, projection=None):
    list_report = []
    async for report in report_client.find(filter, projection).sort("_id"):
        list_report.append(report)

    return list_report

async def get_report(id: str, get_all:bool):
    report = await report_client.find_one({"_id": ObjectId(id)})
    news_ids = report.get("news_ids").copy()
    for heading in report.get("headings"):
        news_ids.extend(heading.get("news_ids"))
        heading["news"] = []
    news_ids = [ObjectId(x) for x in news_ids]
    news_projection = {"_id": True, "data:content": True, "pub_date": True, "data:title":True}
    news_filter = {"_id": {"$in": news_ids}}
    news_dict = {}
    async for news in new_client.find(news_filter, news_projection):
        news["_id"] = str(news["_id"])
        if not get_all:
            news["data:content"] = ".".join(news["data:content"].split(".")[:11])
        news_dict[news["_id"]] = news
    for heading in report.get("headings"):
        for news_id in heading.get("news_ids"):
            heading["news"].append(news_dict.get(news_id))
    report["news"] = []
    for news_id in report.get("news_ids"):
        report["news"].append(news_dict.get(news_id))
    report.pop("news_ids")
    return report

async def create_report(report):
    created_rp = await report_client.insert_one(report)
    return created_rp

async def update_report(id: str, data):
    for heading in data.get("headings"):
        if heading.get("news"):
            heading.pop("news")
    updated_rp = await report_client.update_one({"_id": ObjectId(id)}, {"$set": data})
    return updated_rp

async def delete_report(id: str):
    deleted_rp = await report_client.delete_one({"_id": ObjectId(id)})
    return deleted_rp

async def remove_heading_from_report(id_rp, id_heading: str):
    report_filter = {"_id": ObjectId(id_rp)}
    update_action = {
        "$pull": {
            "headings": {"id": id_heading}
        }
    }
    await report_client.update_one(report_filter, update_action)

async def add_heading_to_report(heading):
    await report_client.update_one({
        "_id": ObjectId(heading.get("report_id"))
    }, {
        "$push": {
            "headings": {
                "id": heading.get("heading_id"),
                "title": heading.get("title"),
                "news_ids": heading.get("news_ids")
            }
        }
    })

async def add_news_to_heading(report_id:str, heading_id:str, news_ids:list[str]):
    if heading_id is None:
        await report_client.update_one({
            "_id": ObjectId(report_id),
        }, {
            "$addToSet": {
                "news_ids": {
                    "$each": news_ids
                }
            }
        })
    else:
        await report_client.update_one({
            "_id": ObjectId(report_id),
            "headings.id": heading_id
        }, {
            "$addToSet": {
                "headings.$.news_ids": {
                    "$each": news_ids
                }
            }
        })

async def remove_news_from_heading(report_id:str, heading_id:str, news_ids:list[str]):
    if heading_id is None:
        await report_client.update_one({
            "_id": ObjectId(report_id),
        }, {
            "$pull": {
                "news_ids": {"$in": news_ids}
            }
        })
    else:
        await report_client.update_one({
            "_id": ObjectId(report_id),
            "headings.id": heading_id
        }, {
            "$pull": {
                "headings.$.news_ids": {"$in": news_ids}
            }
        })