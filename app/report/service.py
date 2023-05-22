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
        # Find the newsletter document by its id_linh_vuc
        newsletter_doc = await newsletter_client.find_one(
            {"_id": ObjectId(data_model.id_linh_vuc)},
            projection
        )
        
        if newsletter_doc and "events" not in newsletter_doc:
            ll = []
            if data_model.start and data_model.end is not None:
            # Convert start and end dates to datetime objects
                start_date = datetime.strptime(data_model.start, "%d/%m/%Y").date()
                datetime_start = datetime.combine(start_date, datetime.min.time())
                
                end_date = datetime.strptime(data_model.end, "%d/%m/%Y").date()
                datetime_end = datetime.combine(end_date, datetime.max.time())
                
                # Query the events collection
                query = {
                    "$or": [
                        {"list_linh_vuc": data_model.id_linh_vuc},
                        {"date_created": {"$gte": datetime_start, "$lte": datetime_end}},
                    ]
                }
                
                async for event_doc in event_client.find(query, projection_event):
                    # Convert date_created field to datetime object
                    if "date_created" in event_doc:
                        try:
                            event_doc["date_created"] = datetime.strptime(event_doc["date_created"], "%d/%m/%Y")
                        except ValueError:
                            pass
                    
                    # Query the news collection and sort by created_at field
                    ll2 = []
                    for new_id in event_doc.get("new_list", []):
                        id_new = {"_id": ObjectId(new_id)}
                        async for new_doc in new_client.find(id_new, projection_new).sort("created_at", -1).limit(data_model.count):
                            try:
                                new_doc["created_at"] = datetime.strptime(new_doc["created_at"], "%Y/%m/%d %H:%M:%S")
                            except ValueError:
                                pass
                            ll2.append(new_doc)
                    
                    # Sort the news list by created_at field and limit to data_model.count
                    ll2 = sorted(ll2, key=lambda x: x.get("created_at"), reverse=True)[:data_model.count]
                    
                    event_doc["new_list"] = ll2             
                    ll.append(event_doc)
            else: 
                # Query the events collection
                query = {
                    "$or": [
                        {"list_linh_vuc": data_model.id_linh_vuc},
                    ]
                }
                
                async for event_doc in event_client.find(query, projection_event):
                    # Convert date_created field to datetime object
                    if "date_created" in event_doc:
                        try:
                            event_doc["date_created"] = datetime.strptime(event_doc["date_created"], "%d/%m/%Y")
                        except ValueError:
                            pass
                    
                    # Query the news collection and sort by created_at field
                    ll2 = []
                    for new_id in event_doc.get("new_list", []):
                        id_new = {"_id": ObjectId(new_id)}
                        async for new_doc in new_client.find(id_new, projection_new).sort("created_at", -1).limit(data_model.count):
                            try:
                                new_doc["created_at"] = datetime.strptime(new_doc["created_at"], "%Y/%m/%d %H:%M:%S")
                            except ValueError:
                                pass
                            ll2.append(new_doc)
                    
                    # Sort the news list by created_at field and limit to data_model.count
                    ll2 = sorted(ll2, key=lambda x: x.get("created_at"), reverse=True)[:data_model.count]
                    
                    event_doc["new_list"] = ll2             
                    ll.append(event_doc)
            
            newsletter_doc["events"] = ll
            
        list_ev.append(newsletter_doc)
    
    return list_ev

