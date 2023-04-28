import asyncio
from typing import List

import pydantic
from bson.objectid import ObjectId
from fastapi import HTTPException, status

from app.event.model import AddNewEvent, CreateEvent
from app.news.services import find_news_by_filter
from db.init_db import get_collection_client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

client = get_collection_client("event")
client2 = get_collection_client("news")
client3 = get_collection_client("event_system")

projection = {"_id": True, "data:title": True, "data:url": True}


async def add_event(event):
    if event["system_created"] == True:
        created_event = await client3.insert_one(event, {"user_id": 0})
        id_event = str(created_event.inserted_id)
        filter_event = await client3.find_one({"_id": ObjectId(id_event)})
        event_name = filter_event["event_name"]
        newsList = event.get("new_list", [])
        await client2.update_many(
            {"_id": {"$in": [ObjectId(event_id) for event_id in newsList]}},
            {"$push": {"event_list": {"event_id": id_event, "event_name": event_name}}},
        )
        
        return created_event
    if event["system_created"] == False:
        created_event = await client.insert_one(event)
        id_event = str(created_event.inserted_id)
        filter_event = await client.find_one({"_id": ObjectId(id_event)})
        event_name = filter_event["event_name"]
        newsList = event.get("new_list", [])
        await client2.update_many(
            {"_id": {"$in": [ObjectId(event_id) for event_id in newsList]}},
            {"$push": {"event_list": {"event_id": id_event, "event_name": event_name}}},
        )
        return created_event


async def get_all_by_paginate(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_event = []

    async for item in client.find(filter).sort("_id").skip(offset).limit(limit):
        ll = []
        for Item in item["new_list"]:
            id_new = {"_id": ObjectId(Item)}
            async for new in client2.find(id_new, projection):
                gg = json(new)
                ll.append(gg)
        item["new_list"] = ll
        item["total_new"] = len(item["new_list"])
        item = json(item)
        list_event.append(item)
    return list_event

async def get_all_by_system(filter, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_event = []

    async for item in client3.find(filter).sort("_id").skip(offset).limit(limit):
        ll = []
        for Item in item["new_list"]:
            id_new = {"_id": ObjectId(Item)}
            async for new in client2.find(id_new, projection):
                gg = json(new)
                ll.append(gg)
        item["new_list"] = ll
        item["total_new"] = len(item["new_list"])
        item = json(item)
        list_event.append(item)
    return list_event

def json(event) -> dict:
    event["_id"] = str(event["_id"])
    return event

async def search_id(user_id: str):
    query = {"user_id": {"$eq": user_id}}
    list_event = []
    async for item in client.find(query).sort("_id"):
        ll = []
        for Item in item["new_list"]:
            id_new = {"_id": ObjectId(Item)}
            async for new in client2.find(id_new, projection):
                gg = json(new)
                ll.append(gg)
        item["new_list"] = ll
        item["total_new"] = len(item["new_list"])
        item = json(item)
        list_event.append(item)
    return list_event

async def search_event(event_name: str, data: ObjectId, chu_the: str, khach_the: str, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    list_event = []
    query = {}
    if event_name:
        query["$or"] = [{"event_name": {"$regex": event_name, "$options": "-i"}}]
    if data:
        query["new_list"] = {"$nin": [data]}
    if chu_the:
        query = {"chu_the": {"$regex": chu_the, "$options": "-i"}}
    if khach_the:
        query = {"khach_the": {"$regex": khach_the, "$options": "-i"}}
    if not query:
        query = {}
    async for item in client.find(query).sort("_id").skip(offset).limit(limit):
        item["total_new"] = len(item["new_list"])
        items = json(item)
        list_event.append(items)
    return list_event


async def search_result(name, id_new, chu_the, khach_the):
    query = {}
    if name:
        query["event_name"] = {"$regex": name, "$options": "-i"}
    if id_new:
        query["new_list"] = {"$nin": [id_new]}
    if chu_the:
        query = {"chu_the": {"$regex": chu_the, "$options": "-i"}}
    if khach_the:
        query = {"khach_the": {"$regex": khach_the, "$options": "-i"}}
    if not query:
        query = {}
    return await client.count_documents(query)


async def event_detail(id) -> dict:
    ev_detail = await client.find_one({"_id": ObjectId(id)})
    new_list = []
    if "new_list" in ev_detail:
        new_list = await find_news_by_filter(
            {"_id": {"$in": convert_map_str_to_object_id(ev_detail["new_list"])}},
            {"_id": 1, "data:title": 1, "data:url": 1},
        )
        ev_detail["new_list"] = new_list
    if ev_detail:
        ev_detail["total_new"] = len(ev_detail["new_list"])
        ev = json(ev_detail)
        return ev

async def event_detail_system(id) -> dict:
    ev_detail = await client3.find_one({"_id": ObjectId(id)})
    new_list = []
    if "new_list" in ev_detail:
        new_list = await find_news_by_filter(
            {"_id": {"$in": convert_map_str_to_object_id(ev_detail["new_list"])}},
            {"_id": 1, "data:title": 1, "data:url": 1},
        )
        ev_detail["new_list"] = new_list
    if ev_detail:
        ev_detail["total_new"] = len(ev_detail["new_list"])
        ev = json(ev_detail)
        return ev

def convert_map_str_to_object_id(array: list[str]):
    return list(map(ObjectId, array))


async def count_event(count):
    return await client.count_documents(count)

async def count_event_system(count):
    return await client3.count_documents(count)

async def update_add(id: str, data):
    event = await client.find_one({"_id": ObjectId(id)})
    event_2 = await client3.find_one({"_id": ObjectId(id)})
    
    if event:
        event_name = event["event_name"]
        newsList = data.get("new_list", [])
        exist_event = await client.find_one({"event_name": data["event_name"]})
        if exist_event:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="event already exist"
            )
        await client.insert_one(data)
        await client2.update_many(
            {"event_list.event_id": id, "event_list.event_name": event_name},
            {"$pull": {"event_list": {"event_id": id, "event_name": event_name}}},
        )
        for new in newsList:
            new_id = new
            await client2.update_one(
                {"_id": ObjectId(new_id)},
                {
                    "$addToSet": {
                        "event_list": {"event_id": id, "event_name": event_name}
                    }
                },
            )
    if event_2:
        event_name_2 = event_2["event_name"]
        newsList_2 = data.get("new_list", [])
        exist_event_2 = await client3.find_one({"event_name": data["event_name"]})
        if exist_event_2:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="event already exist"
            )
        await client3.insert_one(data)
        await client2.update_many(
            {"event_list.event_id": id, "event_list.event_name": event_name_2},
            {"$pull": {"event_list": {"event_id": id, "event_name": event_name_2}}},
        )
        for new in newsList_2:
            new_id = new
            await client2.update_one(
                {"_id": ObjectId(new_id)},
                {
                    "$addToSet": {
                        "event_list": {"event_id": id, "event_name": event_name}
                    }
                },
            )
    
async def update_event(id: str, data: dict):
    id_event = str(id)
    event = await client.find_one({"_id": ObjectId(id)})
    event_2 = await client3.find_one({"_id": ObjectId(id)})
    
    list_event_1 = await client.find().to_list(length=None)
    list_event_2 = await client3.find().to_list(length=None)
    
    if event:
        event_name = event["event_name"]
        newsList = data.get("new_list", [])
        
        await client2.update_many(
            {"event_list.event_id": id_event, "event_list.event_name": event_name},
            {"$pull": {"event_list": {"event_id": id_event, "event_name": event_name}}},
        )
        for new in newsList:
            new_id = new
            await client2.update_one(
                {"_id": ObjectId(new_id)},
                {
                    "$addToSet": {
                        "event_list": {"event_id": id_event, "event_name": event_name}
                    }
                },
            )
        for item in list_event_1:
            if item["_id"] != event["_id"] and item["event_name"] == data["event_name"]: 
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="event is duplicated")
            
        updated_event = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_event:
            return status.HTTP_200_OK
        return False
            
    if event_2:
        event_name_2 = event_2["event_name"]
        newsList = data.get("new_list", [])
        
        await client2.update_many(
            {"event_list.event_id": id_event, "event_list.event_name": event_name_2},
            {"$pull": {"event_list": {"event_id": id_event, "event_name": event_name_2}}},
        )
        for new in newsList:
            new_id = new
            await client2.update_one(
                {"_id": ObjectId(new_id)},
                {
                    "$addToSet": {
                        "event_list": {"event_id": id_event, "event_name": event_name_2}
                    }
                },
            )
        for item in list_event_2:
            if item["_id"] != event_2["_id"] and item["event_name"] == data["event_name"]: 
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="event is duplicated")
            
        updated_event = await client3.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_event:
            return status.HTTP_200_OK
        return False


async def add_list_new_id(id: str, id_new: List[ObjectId]):
    id_event = str(id)
    filter_event = await client3.find_one({"_id": ObjectId(id_event)})
    filter_event_2 = await client.find_one({"_id": ObjectId(id_event)})
    
    if filter_event:
        event_name = filter_event["event_name"]
        newList = []
        for item in id_new:
            newList.append(item)
        await client2.update_many(
            {"_id": {"$in": [ObjectId(event_id) for event_id in newList]}},
            {"$addToSet": {"event_list": {"event_id": id_event, "event_name": event_name}}},
        )
        return await client3.update_one(
            {"_id": ObjectId(id)}, {"$push": {"new_list": {"$each": id_new}}}
        )
    if filter_event_2:
        event_name_2 = filter_event_2["event_name"]
        newList = []
        for item in id_new:
            newList.append(item)
        await client2.update_many(
            {"_id": {"$in": [ObjectId(event_id) for event_id in newList]}},
            {"$addToSet": {"event_list": {"event_id": id_event, "event_name": event_name_2}}},
        )
        return await client.update_one(
            {"_id": ObjectId(id)}, {"$push": {"new_list": {"$each": id_new}}}
        )


async def add_list_event_id(id_new: str, list_id_event: List[ObjectId]):
    id_news = str(id_new)
    eventList = []
    for item in list_id_event:
        eventList.append(item)
       
    event_ids = [ObjectId(event_id) for event_id in list_id_event]
    ev_name = await client.find({"_id": {"$in": event_ids}}).to_list(length=None)
    ev_name_2 = await client3.find({"_id": {"$in": event_ids}}).to_list(length=None)
    
    for item2 in ev_name_2:
        if item2:
            ev_id_2 = str(item2["_id"])
            await client2.update_many(
                {"_id": ObjectId(id_news)},
                {
                    "$addToSet": {
                        "event_list": {"event_id": ev_id_2, "event_name": item2["event_name"]}
                    }
                },
            ),
            await client3.update_many(
                {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
                {"$addToSet": {"new_list": id_news}},
            )
    
    for item in ev_name:
        if item:
            ev_id = str(item["_id"])
            await client2.update_many(
                {"_id": ObjectId(id_news)},
                {
                    "$addToSet": {
                        "event_list": {"event_id": ev_id, "event_name": item["event_name"]}
                    }
                },
            ),
            await client.update_many(
                {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
                {"$addToSet": {"new_list": id_news}},
            ),
            
        for item2 in ev_name_2:
            if item2:
                ev_id_2 = str(item2["_id"])
                await client2.update_many(
                    {"_id": ObjectId(id_news)},
                    {
                        "$addToSet": {
                            "event_list": {"event_id": ev_id_2, "event_name": item2["event_name"]}
                        }
                    },
                ),
                await client3.update_many(
                    {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
                    {"$addToSet": {"new_list": id_news}},
                )
                
            if item and item2:
                ev_id = str(item["_id"])
                ev_id_2 = str(item2["_id"])
                await asyncio.gather(
                    client3.update_many(
                        {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
                        {"$addToSet": {"new_list": id_news}},
                    ),
                    client.update_many(
                        {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
                        {"$addToSet": {"new_list": id_news}},
                    ),
                    client2.update_many(
                        {"_id": ObjectId(id_news)},
                        {
                            "$addToSet": {
                                "event_list":{
                                    "$each": [
                                        {"event_id": ev_id, "event_name": item["event_name"]},
                                        {"event_id": ev_id_2, "event_name": item2["event_name"]},  
                                    ]
                                }
                            }
                        },
                    ),
                )
        
            
                

async def remove_list_new_id(id: str, id_new: List[ObjectId]):
    id_event = str(id)
    filter_event = await client3.find_one({"_id": ObjectId(id_event)})
    filter_event_2 = await client.find_one({"_id": ObjectId(id_event)})
    
    if filter_event:
        event_name = filter_event["event_name"]
        newList = []
        for item in id_new:
            newList.append(item)
        await client2.update_many(
            {"event_list.event_id": id_event, "event_list.event_name": event_name},
            {"$pull": {"event_list": {"event_id": id_event, "event_name": event_name}}},
        )
        return await client3.update_one(
            {"_id": ObjectId(id)}, {"$pull": {"new_list": {"$in": id_new}}}
        )
    if filter_event_2:
        event_name_2 = filter_event_2["event_name"]
        newList = []
        for item in id_new:
            newList.append(item)
        await client2.update_many(
            {"event_list.event_id": id_event, "event_list.event_name": event_name_2},
            {"$pull": {"event_list": {"event_id": id_event, "event_name": event_name_2}}},
        )
        return await client.update_one(
            {"_id": ObjectId(id)}, {"$pull": {"new_list": {"$in": id_new}}}
        )

async def remove_list_event_id(id: str, list_id_event: List[ObjectId]):
    id_new = str(id)
    eventList = []
    for item in list_id_event:
        eventList.append(item)
    ev_name = await client.find_one(
        {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}}
    )
    ev_name_2 = await client3.find_one(
        {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}}
    )
    if ev_name_2:
        ev_id_2 = str(ev_name_2["_id"])
        await client2.update_many(
            {"event_list.event_id": ev_id_2, "event_list.event_name": ev_name_2["event_name"]},
            {
                "$pull": {
                    "event_list": {"event_id": ev_id_2, "event_name": ev_name_2["event_name"]}
                }
            },
        )
        return await client3.update_one(
            {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
            {"$pull": {"new_list": id_new}},
        )
    if ev_name:
        ev_id = str(ev_name["_id"])
        await client2.update_many(
            {"event_list.event_id": ev_id, "event_list.event_name": ev_name["event_name"]},
            {
                "$pull": {
                    "event_list": {"event_id": ev_id, "event_name": ev_name["event_name"]}
                }
            },
        )
        return await client.update_one(
            {"_id": {"$in": [ObjectId(event_id) for event_id in eventList]}},
            {"$pull": {"new_list": id_new}},
        )

async def add_list_new(id: str, data: List[AddNewEvent]):
    list_ev = []
    for Data in data:
        list_ev.append(
            {
                "id_new": Data.id_new,
                "data_title": Data.data_title,
                "data_url": Data.data_url,
            }
        )
    return await client.update_one(
        {"_id": ObjectId(id)},
        {"$addToSet": {"new_list": {"$each": [Data.dict() for Data in data]}}},
    )


async def delete_list_new(id: str, data: List[AddNewEvent]):
    docs = [dict(Data) for Data in data]
    return await client.update_one(
        {"_id": ObjectId(id)}, {"$pull": {"new_list": {"$in": docs}}}
    )


async def delete_event(id):
    event = await client.find_one({"_id": ObjectId(id)})
    event_2 = await client3.find_one({"_id": ObjectId(id)})
    
    if event:
        await client.delete_one({"_id": ObjectId(id)})
        return 200
    if event_2:
        await client3.delete_one({"_id": ObjectId(id)})
        return 200
