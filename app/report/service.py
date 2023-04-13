import pydantic
from bson.objectid import ObjectId
from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


client = get_collection_client("report")


async def count(filter):
    return await client.count_documents(filter)


async def get_all(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_report = []
    async for report in client.find(filter).sort("_id").skip(offset).limit(limit):
        list_report.append(report)

    return list_report


async def get_by_id(id: str):
    return await client.find_one({"_id": ObjectId(id)})


async def create_report(report):
    return await client.insert_one(report)


async def update_report(id: str, report: dict):
    return await client.update_one({"_id": ObjectId(id)}, {"$set": report})


async def delete_report(id: str):
    return await client.delete_one({"_id": ObjectId(id)})
