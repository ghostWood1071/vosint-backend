import pydantic
from bson.objectid import ObjectId

from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


report_client = get_collection_client("report")
events_client = get_collection_client("events")
event_client = get_collection_client("event")
event_system_client = get_collection_client("event_system")


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


async def get_events(id: str):
    return await events_client.find_one({"_id": ObjectId(id)})


async def create_events(event):
    return await events_client.insert_one(event)


async def update_events(id: str, event: dict):
    return await events_client.update_one({"_id": ObjectId(id)}, {"$set": event})


async def delete_events(id: str):
    return await events_client.delete_one({"_id": ObjectId(id)})


async def add_event_ids_to_events(id: str, event_ids: list[str]):
    return await events_client.update_one(
        {"_id": ObjectId(id)}, {"$addToSet": {"event_ids": {"$each": event_ids}}}
    )


async def remove_event_ids_in_events(id: str, event_ids: list[str]):
    return await events_client.update_one(
        {"_id": ObjectId(id)}, {"$pullAll": {"event_ids": event_ids}}
    )
