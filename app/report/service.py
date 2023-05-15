from datetime import datetime, time, timedelta

import pydantic
from bson.objectid import ObjectId
from dateutil import parser

from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


report_client = get_collection_client("report")
event_client = get_collection_client("event")
event_system_client = get_collection_client("event_system")
new_client = get_collection_client("news")
newsletter_client = get_collection_client("newsletter")

projection = {
    "_id": True,
    "title": True,
    "parent_id": True,
}

projection_event = {
    "event_name": True,
    "new_list": True,
    "date_created": True
}

projection_new = {
    "_id": True, 
    "data:title": True, 
    "data:url": True, 
    "created_at": True
}

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


async def get_report(id: str):
    return await report_client.find_one({"_id": ObjectId(id)})


async def create_report(report):
    return await report_client.insert_one(report)


async def update_report(id: str, report: dict):
    return await report_client.update_one({"_id": ObjectId(id)}, {"$set": report})


async def delete_report(id: str):
    return await report_client.delete_one({"_id": ObjectId(id)})

async def get_event(data):
    list_ev = []
    for data_model in data:
        async for item in newsletter_client.find({"_id": ObjectId(data_model.id_linh_vuc)}, projection):
            if "events" not in item:
                ll = []
                start_date = datetime.strptime(data_model.start, "%d/%m/%Y").date()
                datetime_start = datetime.combine(start_date, time.min)
                
                end_date = datetime.strptime(data_model.end, "%d/%m/%Y").date()
                datetime_end = datetime.combine(end_date, time.max)
                query = {"$or": 
                    [
                        {"list_linh_vuc": {"$in": [data_model.id_linh_vuc]}},
                        {"date_created": {
                            "$gte": datetime_start,
                            "$lt": datetime_end
                        }},
                    ]
                }
                async for item2 in event_client.find(
                    query,
                    projection_event
                ):
                    item2["date_created"] = datetime.strptime(item2["date_created"], "%d/%m/%Y")
                    ll2 = []
                    for item3 in item2["new_list"]:
                        id_new = {"_id": ObjectId(item3)}
                        async for new in new_client.find(id_new, projection_new).sort("created_at", -1).limit(data_model.count):
                            new["created_at"] = datetime.strptime(new["created_at"], "%Y/%m/%d %H:%M:%S")
                            ll2.append(new)
                    ll2 = sorted(ll2, key=lambda x: x["created_at"], reverse=True)[:data_model.count]
                    item2["new_list"] = ll2             
                    ll.append(item2)
                item["events"] = ll
        list_ev.append(item)
    return list_ev

