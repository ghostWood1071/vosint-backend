from typing import List

import pydantic
from bson.objectid import ObjectId
from fastapi import HTTPException, status

from app.event.model import AddNewEvent
from app.news.services import find_news_by_filter_and_paginate
from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

client = get_collection_client("event")
client2 = get_collection_client("news")

projection = {
    "_id": True,
    "data:title": True,
    "data:url": True
}


async def add_event(event):
    created_event = await client.insert_one(event)
    id_event = str(created_event.inserted_id)
    filter_event = await client.find_one({"_id": ObjectId(id_event)})
    event_name = filter_event["event_name"]
    newsList = event.get("new_list", [])
    await client2.update_many(
        {
            "_id": {
                "$in": [ObjectId(event_id) for event_id in newsList]
            }
        },
        {
            "$push": {
                "event_list": {
                    "event_id": id_event,
                    "event_name": event_name
                }
            }
        }
    )
    return await client.find_one({"id": created_event.inserted_id})


async def get_all_by_paginate(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_event = []
    
    async for item in client.find(filter).sort("_id").skip(offset).limit(limit):
        for Item in item["new_list"]:
            id_new = {"_id": ObjectId(Item)}
            ll = item["new_list"] = []
            async for new in client2.find(id_new, projection):
                print(new)
                gg = json(new)
                ll.append(gg)
                
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
    id_event = str(id)
    event = await client.find_one({"_id": ObjectId(id)})
    event_name = event["event_name"]
    newsList = data.get("new_list", [])
    await client2.update_many(
        {
            "event_list.event_id": id_event,
            "event_list.event_name": event_name
        },
        {
            "$pull": {
                "event_list": {
                    "event_id": id_event,
                    "event_name": event_name
                }
            }
        }
    )
    for new in newsList:
        new_id = new
        await client2.update_one(
            {"_id": ObjectId(new_id)},
            {
                "$addToSet": {
                    "event_list": {
                        "event_id": id_event,
                        "event_name": event_name
                    }
                }
            }
        )
    
    updated_event = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
    if updated_event:
        return status.HTTP_200_OK
    return False


async def add_list_new_id(id: str, id_new: List[ObjectId]):
    id_event = str(id)
    filter_event = await client.find_one({"_id": ObjectId(id_event)})
    event_name = filter_event["event_name"]
    newList = []
    for item in id_new:
        newList.append(item)
    await client2.update_many(
        { "_id": { "$in": [ObjectId(event_id) for event_id in newList] } },
        {
            "$addToSet": {
                "event_list": {
                    "event_id": id_event,
                    "event_name": event_name
                }
            }
        }
    )
    return await client.update_one(
        {"_id": ObjectId(id)}, {"$push": {"new_list": {"$each": id_new}}}
    )
    
async def add_list_event_id(id_new: str, list_id_event: List[ObjectId]):
    id_news = str(id_new)
    filter_event = await client2.find_one({"_id": ObjectId(id_news)})
    eventList = []
    for item in list_id_event:
        eventList.append(item)
    ev_name = await client.find_one({"_id": { "$in": [ObjectId(event_id) for event_id in eventList] }})
    ev_id = str(ev_name["_id"])
    await client2.update_many(
        {   "_id": ObjectId(id_new) },
        {
            "$addToSet": {
                "event_list": {
                    "event_id": ev_id ,
                    "event_name": ev_name["event_name"]
                }
            }
        }
    )
    return await client.update_one(
        {"_id": { "$in": [ObjectId(event_id) for event_id in eventList] }}, {"$push": {"new_list": id_news}}
    )
    
async def remove_list_new_id(id: str, id_new: List[ObjectId]):
    id_event = str(id)
    filter_event = await client.find_one({"_id": ObjectId(id_event)})
    event_name = filter_event["event_name"]
    newList = []
    for item in id_new:
        newList.append(item)
    await client2.update_many(
        {
            "event_list.event_id": id_event,
            "event_list.event_name": event_name
        },
        {
            "$pull": {
                "event_list": {
                    "event_id": id_event,
                    "event_name": event_name
                }
            }
        }
    )
    return await client.update_one(
        {"_id": ObjectId(id)}, {"$pull": {"new_list": {"$in": id_new}}}
    )
    
async def remove_list_event_id(id: str, list_id_event: List[ObjectId]):
    id_new = str(id)
    eventList = []
    for item in list_id_event:
        eventList.append(item)
    ev_name = await client.find_one({"_id": { "$in": [ObjectId(event_id) for event_id in eventList] }})
    ev_id = str(ev_name["_id"])
    await client2.update_many(
        {
            "event_list.event_id": ev_id,
            "event_list.event_name": ev_name["event_name"]
        },
        {
            "$pull": {
                "event_list": {
                    "event_id": ev_id,
                    "event_name": ev_name["event_name"]
                }
            }
        }
    )
    return await client.update_one(
        {"_id": { "$in": [ObjectId(event_id) for event_id in eventList] }}, {"$pull": {"new_list": id_new}}
    )
    
async def add_list_new(id: str, data: List[AddNewEvent]):
    list_ev = []
    for Data in data:
        list_ev.append(
            {"id_new": Data.id_new, "data_title": Data.data_title, "data_url": Data.data_url}
        )
    return await client.update_one(
        {"_id": ObjectId(id)},
        {"$addToSet": {"new_list": {"$each": [Data.dict() for Data in data]}}}
    )
    
async def delete_list_new(id: str, data: List[AddNewEvent]):    
    docs = [dict(Data) for Data in data]
    return await client.update_one(
        {"_id": ObjectId(id)}, {"$pull": {"new_list": {"$in": docs}}}
    )
    
async def delete_event(id):
    event = await client.find_one({"_id": ObjectId(id)})
    if event:
        await client.delete_one({"_id": ObjectId(id)})
        return 200



