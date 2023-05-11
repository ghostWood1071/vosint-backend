import pydantic
from bson.objectid import ObjectId

from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


report_client = get_collection_client("report")
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
