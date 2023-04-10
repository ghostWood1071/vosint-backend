from typing import List

import pydantic
from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

client = get_collection_client("event")


async def add_event(event):
    return await client.insert_one(event)


async def get_all_by_paginate(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_event = []
    async for item in client.find(filter).sort("_id").skip(offset).limit(limit):
        item = json(item)
        list_event.append(item)
    return list_event


async def get(list):
    list_event = []
    async for item in client.find(list).sort("_id"):
        item = json(item)
        list_event.append(item)
    return list_event


def json(event) -> dict:
    event["_id"] = str(event["_id"])
    return event

async def search_event(event: str, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_event = []
    async for item in client.find(
        {"$or": [{"event_name": {"$regex": event, "$options": "i"}}]}
    ).sort("_id").skip(offset).limit(limit):
        item = json(item)
        list_event.append(item)
    return list_event

async def search_result(name):
    filter = {"event_name": {"$regex": name, "$options": "i"}}
    return await client.count_documents(filter)


async def event_detail(id) -> dict:
    ev_detail = await client.find_one({"_id": ObjectId(id)})
    if ev_detail:
        ev = json(ev_detail)
        return ev
    

async def count_event(count):
    return await client.count_documents(count)


async def update_event(id: str, data: dict):
    event = await client.find_one({"_id": ObjectId(id)})
    if event:
        updated_event = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_event:
            return status.HTTP_200_OK
        return False


async def add_list_infor(id: str, id_infor: List[ObjectId]):
    return await client.update_one(
        {"_id": ObjectId(id)}, {"$push": {"new_list": {"$each": id_infor}}}
    )


async def delete_event(id):
    event = await client.find_one({"_id": ObjectId(id)})
    if event:
        await client.delete_one({"_id": ObjectId(id)})
        return 200
