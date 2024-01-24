from typing import List
from bson.objectid import ObjectId
from db.init_db import get_collection_client

client = get_collection_client("users")


async def create_user(user):
    subject_client = get_collection_client("subjects")
    subject_ids = []
    async for subject in subject_client.find ({}, {"_id": True}):
        subject_ids.append(str(subject["_id"]))
    user["subject_ids"] = subject_ids
    created_user = await client.insert_one(user)
    return await client.find_one({"id": created_user.inserted_id})


async def read_user_by_username(username: str):
    return await client.find_one({"username": username})


async def update_user(user_id: ObjectId, user):
    return await client.update_one({"_id": user_id}, {"$set": user})


async def get_users(filter_spec, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    users = []
    async for new in client.find(filter_spec).sort("_id").skip(offset).limit(limit):
        new = user_entity(new)
        users.append(new)

    return users


async def count_users(filter_spec):
    return await client.count_documents(filter_spec)


async def get_user_by_id(id: ObjectId):
    return await client.find_one({"_id": id})


async def get_user(id: str) -> dict:
    users = await client.find_one({"_id": ObjectId(id)})
    if users:
        return user_entity(users)


async def find_user_by_id(user_id: str):
    return await client.find_one({"_id": user_id})


async def update_bookmark_user(id: ObjectId, datas: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$push": {"news_bookmarks": {"$each": datas}}}
    )


async def delete_bookmark_user(id: ObjectId, id_bookmarks: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$pull": {"news_bookmarks": {"$in": id_bookmarks}}}
    )


async def update_vital_user(id: ObjectId, vitals: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$push": {"vital_list": {"$each": vitals}}}
    )


async def delete_vital_user(id: ObjectId, id_vitals: List[ObjectId]):
    return await client.update_one(
        {"_id": id}, {"$pull": {"vital_list": {"$in": id_vitals}}}
    )


async def update_interested_object(
    user_id: ObjectId, interested_objects: List[ObjectId]
):
    return await client.update_one(
        {"_id": user_id}, {"$push": {"interested_list": {"$each": interested_objects}}}
    )


async def delete_item_from_interested_list(
    user_id: str, id_interesteds: List[ObjectId]
):
    return await client.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"interested_list": {"$in": id_interesteds}}},
    )


async def get_interested_list(social_name):
    pipeline = [
        {"$match": {"interested_list.social_name": {"$regex": social_name}}},
        {"$project": {"_id": 0, "interested_list": 1}},
        {"$unwind": "$interested_list"},
        {"$match": {"interested_list.social_name": {"$regex": social_name}}},
    ]
    cursor = client.aggregate(pipeline)
    interested_list = []
    async for document in cursor:
        interested_list.append(document["interested_list"])
    return interested_list


async def delete_user(id: str):
    user = await client.find_one({"_id": ObjectId(id)})
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True


async def get_vital_ids(id: ObjectId):
    user = await client.find_one({"_id": ObjectId(id)})
    vital_ids = [str(vital_id) for vital_id in user["vital_list"]]
    return vital_ids


def user_entity(user) -> dict:
    news_bookmarks = []
    vital_list = []
    interested_list = []
    subject_list = []
    follow_list=[]

    if "vital_list" in user:
        for news_id in user["vital_list"]:
            vital_list.append(str(news_id))

    if "news_bookmarks" in user:
        for news_id in user["news_bookmarks"]:
            news_bookmarks.append(str(news_id))

    if "interested_list" in user:
        for object_id in user["interested_list"]:
            interested_list.append(str(object_id))

    if "subject_ids" in user:
        for subject_id in user["subject_ids"]:
            subject_list.append(str(subject_id))

    if "following" in user:
        for follow_id in user["following"]:
            follow_list.append(str(follow_id))

    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
        "news_bookmarks": news_bookmarks,
        "vital_list": vital_list,
        "interested_list": interested_list,
        "avatar_url": user["avatar_url"] if "avatar_url" in user else None,
        
        "subject_list": subject_list,
        "follow_list": follow_list,
    }
