from typing import List
from typing import Optional
from bson import ObjectId
from fastapi import status

from app.social_media.models import AddFollowed, UpdateSocial, UpdateStatus
from app.social_media.utils import object_to_json
from db.init_db import get_collection_client
from vosint_ingestion.models import MongoRepository
from datetime import datetime, timedelta

client = get_collection_client("social_media")
client2 = get_collection_client("socials")
facebook_client = get_collection_client("facebook")
twitter_client = get_collection_client("twitter")
tiktok_client = get_collection_client("tiktok")


async def create_social_media(user):
    created_user = await client.insert_one(user)
    new_user_id = str(created_user.inserted_id)
    filter_result = await client.find_one({"_id": ObjectId(new_user_id)})
    social_name = filter_result["social_name"]
    # update the users_follow list for each follower
    followers = user.get("followed_by", [])
    await client2.update_many(
        {
            "_id": {
                "$in": [ObjectId(follower.get("followed_id")) for follower in followers]
            }
        },
        {
            "$push": {
                "users_follow": {
                    "follow_id": new_user_id,
                    "social_name": social_name,
                }
            }
        },
    )
    return await client.find_one({"id": created_user.inserted_id})


async def delete_user_by_id(id: str):
    str_id = str(id)
    user = await client.find_one({"_id": ObjectId(id)})
    social_name = user["social_name"]
    followers = []
    filter_object = user.get("followed_by")
    for filter_list in filter_object:
        followers.append(
            {
                "followed_id": str(filter_list.get("followed_id")),
                "username": str(filter_list.get("username")),
            }
        )
    await client2.update_many(
        {"_id": {"$in": [ObjectId(f["followed_id"]) for f in followers]}},
        {
            "$pull": {
                "users_follow": {
                    "follow_id": str_id,
                    "social_name": social_name,
                }
            }
        },
    )
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True


async def update_social_account(data: UpdateSocial):
    _id = data["id"]
    user_id = str(_id)
    socials = await client.find_one({"_id": ObjectId(_id)})
    social_name = socials["social_name"]
    compare_name = data["social_name"]
    if social_name != compare_name:
        social_name = compare_name
    followers = data.get("followed_by", [])

    await client2.update_many(
        {
            "followed_by.followed_id": user_id,
            "followed_by.username": compare_name,
        },
        {
            "$pull": {
                "followed_by": {
                    "followed_id": user_id,
                    "username": compare_name,
                }
            }
        },
    )

    for follower in followers:
        follower_id = follower.get("follow_id")
        await client2.update_one(
            {"_id": ObjectId(follower_id)},
            {
                "$addToSet": {
                    "users_follow": {
                        "follow_id": user_id,
                        "social_name": social_name,
                    }
                }
            },
        )

    data_copy = data.copy()
    data_copy.pop("id")

    return await client.update_one(
        {"_id": ObjectId(_id)},
        {"$set": data_copy},
    )


async def update_status_account(id: str, data: UpdateStatus):
    socials = await client.find_one({"_id": ObjectId(id)})
    if socials:
        updated_status = await client.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_status:
            return status.HTTP_200_OK
        return False


async def update_followed_by(id: str, data: List[AddFollowed]):
    user_id = str(id)
    filter_result = await client.find_one({"_id": ObjectId(id)})
    social_name = filter_result["social_name"]
    followers = []
    for datum in data:
        followers.append({"followed_id": datum.followed_id, "username": datum.username})
    await client2.update_many(
        {"_id": {"$in": [ObjectId(f["followed_id"]) for f in followers]}},
        {
            "$addToSet": {
                "users_follow": {
                    "follow_id": user_id,
                    "social_name": social_name,
                }
            }
        },
    )
    return await client.update_one(
        {"_id": ObjectId(id)},
        {"$addToSet": {"followed_by": {"$each": [datum.dict() for datum in data]}}},
    )


async def delete_followed_by(id: str, data: List[AddFollowed]):
    user_id = str(id)
    filter_result = await client.find_one({"_id": ObjectId(id)})
    social_name = filter_result["social_name"]
    followers = []
    for datum in data:
        followers.append(
            {
                "followed_id": str(datum.followed_id),
                "username": datum.username,
            }
        )
    await client2.update_many(
        {"_id": {"$in": [ObjectId(f["followed_id"]) for f in followers]}},
        {
            "$pull": {
                "users_follow": {
                    "follow_id": user_id,
                    "social_name": social_name,
                }
            }
        },
    )
    docs = [dict(datum) for datum in data]
    return await client.update_one(
        {"_id": ObjectId(id)}, {"$pull": {"followed_by": {"$in": docs}}}
    )


async def find_object_by_filter_and_paginate(filter_object, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    objects = []
    async for new in client.find(filter_object).sort("_id").skip(offset).limit(limit):
        new = object_to_json(new)
        objects.append(new)

    return objects


async def find_object_by_filter(filter_object):
    objects = []
    data = client.find(filter_object).sort("_id")

    # result = []
    # async for record in data:
    #     record["_id"] = str(record["_id"])
    #     print("record", record)
    #     result.append(record)
    # return result

    # print(filter_object)
    async for new in client.find(filter_object).sort("_id"):
        new = object_to_json(new)
        objects.append(new)

    return objects


async def count_object(filter_object):
    return await client.count_documents(filter_object)


def social_entity(socials) -> dict:
    return {
        "_id": str(socials["_id"]),
        "social_name": socials["social_name"],
        "social_media": socials["social_media"],
        "social_type": socials["social_type"],
        "account_link": socials["account_link"],
        "avatar_url": socials["avatar_url"],
        "profile": socials["profile"],
        "is_active": bool(socials["is_active"]),
        "followed_by": socials["followed_by"],
    }


async def check_read_socials(post_ids: List[str], social_platform: str, user_id):
    post_id_list = [ObjectId(post_id) for post_id in post_ids]
    filter_spec = {
        "_id": {"$in": post_id_list},
        "list_user_read": {"$not": {"$all": [user_id]}},
    }
    update_command = {"$push": {"list_user_read": user_id}}
    collection = (
        "facebook"
        if social_platform == "facebook"
        else ("twitter" if social_platform == "twitter" else "tiktok")
    )

    return MongoRepository().update_many(collection, filter_spec, update_command)


async def check_unread_socials(post_ids: List[str], social_platform: str, user_id: str):
    post_id_list = [ObjectId(post_id) for post_id in post_ids]
    filter_spec = {"_id": {"$in": post_id_list}}
    update_command = {"$pull": {"list_user_read": {"$in": [user_id]}}}
    collection = (
        "facebook"
        if social_platform == "facebook"
        else ("twitter" if social_platform == "twitter" else "tiktok")
    )
    return MongoRepository().update_many(collection, filter_spec, update_command)


async def feature_keywords(k: int, start_date: str, end_date: str, name: str):
    start_date = datetime(
        int(start_date.split("/")[2]),
        int(start_date.split("/")[1]),
        int(start_date.split("/")[0]),
    )

    end_date = datetime(
        int(end_date.split("/")[2]),
        int(end_date.split("/")[1]),
        int(end_date.split("/")[0]),
    )

    end_date = end_date.replace(hour=23, minute=59, second=59)

    start_date = str(start_date).replace("-", "/")
    end_date = str(end_date).replace("-", "/")

    pipeline = [
        {"$match": {"created_at": {"$gte": start_date, "$lte": end_date}}},
        {"$unwind": {"path": "$keywords"}},
        {
            "$group": {"_id": "$keywords", "value": {"$sum": 1}},
        },
        {"$sort": {"value": -1}},
        {"$limit": k},
    ]

    collection_client = (
        facebook_client
        if name == "facebook"
        else (twitter_client if name == "twitter" else tiktok_client)
    )

    data = collection_client.aggregate(pipeline)

    result = []
    async for record in data:
        result.append(record)

    return result


async def get_news_facebook(news_ids: List[str]):
    filters = [ObjectId(n_id) for n_id in news_ids]
    results = []
    async for row in facebook_client.find({"_id": {"$in": filters}}):
        results.append(row)
    return results


async def social_personal(id: str):
    pipeline = [{"$match": {"$expr": {"$eq": ["$_id", {"$toObjectId": id}]}}}]

    data = client.aggregate(pipeline)

    result = {}
    async for record in data:
        result = record

    return result


async def statistic_interaction(name: str):
    date_current = datetime.now()
    date_ago = date_current - timedelta(days=7)

    date_current = date_current.replace(hour=23, minute=59, second=59)

    date_current = str(date_current).replace("-", "/")
    date_ago = str(date_ago).replace("-", "/")

    pipeline = [
        {"$match": {"created_at": {"$gte": date_ago, "$lte": date_current}}},
        {
            "$group": {
                "_id": {
                    "$substr": ["$created_at", 0, 10],
                },
                "total_like": {"$sum": {"$toInt": "$like"}},
                "total_share": {"$sum": {"$toInt": "$share"}},
            }
        },
        {"$limit": 7},
        {"$sort": {"_id": 1}},
    ]

    collection_client = (
        facebook_client
        if name == "facebook"
        else (twitter_client if name == "twitter" else tiktok_client)
    )

    data = collection_client.aggregate(pipeline)

    result = []
    async for record in data:
        result.append(record)

    return result


async def active_member(name: str):
    # person post the most
    pipeline = [
        {
            "$group": {"_id": "$id_social", "value": {"$sum": 1}},
        },
        {
            "$lookup": {
                "from": "social_media",
                "localField": "_id",
                "foreignField": "_id",
                "as": "user",
            }
        },
        {"$sort": {"value": -1}},
    ]

    collection_client = (
        facebook_client
        if name == "facebook"
        else (twitter_client if name == "twitter" else tiktok_client)
    )

    data = collection_client.aggregate(pipeline)

    result = []
    async for record in data:
        result.append(record)

    return result


async def posts_from_priority(
    id_social, text_search, page_number, page_size, start_date, end_date, sac_thai
):
    filter_spec = {}
    skip = int(page_size) * (int(page_number) - 1)

    # filter by text_search
    if text_search != "":
        filter_spec.update({"$text": {"$search": text_search}})

    # filter by start_date, end_date, text_search
    if start_date:
        start_date = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )
        start_date = str(start_date).replace("-", "/")

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_date = end_date.replace(hour=23, minute=59, second=59)
        end_date = str(end_date).replace("-", "/")

    if start_date != "" and end_date != "":
        filter_spec.update({"created_at": {"$gte": start_date, "$lte": end_date}})

    elif start_date != "":
        filter_spec.update({"created_at": {"$gte": start_date}})

    elif end_date != "":
        filter_spec.update({"created_at": {"$lte": end_date}})

    if sac_thai != "" and sac_thai != "all":
        filter_spec.update({"sentiment": sac_thai})

    filter_spec.update({"$expr": {"$eq": ["$id_social", {"$toObjectId": id_social}]}})

    pipeline = [
        {"$match": {"$expr": {"$eq": ["$_id", {"$toObjectId": id_social}]}}},
        {
            "$lookup": {
                "from": "facebook",
                "pipeline": [{"$match": filter_spec}],
                "as": "facebook_list",
            }
        },
        {
            "$lookup": {
                "from": "twitter",
                "pipeline": [{"$match": filter_spec}],
                "as": "twitter_list",
            }
        },
        {
            "$lookup": {
                "from": "tiktok",
                "pipeline": [{"$match": filter_spec}],
                "as": "tiktok_list",
            }
        },
        {
            "$project": {
                "post_list": {
                    "$slice": [
                        {
                            "$concatArrays": [
                                "$facebook_list",
                                "$twitter_list",
                                "$tiktok_list",
                            ],
                        },
                        int(skip),
                        int(50),
                    ],
                },
            },
        },
        {"$unwind": "$post_list"},
        {"$sort": {"post_list.created_at": -1}},
        {"$group": {"_id": "$_id", "post_list": {"$push": "$post_list"}}},
    ]

    data = client.aggregate(pipeline)

    result = []
    async for record in data:
        result.append(record)

    return result


async def statistic_interaction_from_priority(id_social: str):
    pipeline = [
        {"$match": {"_id": ObjectId(id_social)}},
        {
            "$lookup": {
                "from": "facebook",
                "localField": "_id",
                "foreignField": "id_social",
                "as": "facebook_list",
            }
        },
        {
            "$lookup": {
                "from": "twitter",
                "localField": "_id",
                "foreignField": "id_social",
                "as": "twitter_list",
            }
        },
        {
            "$lookup": {
                "from": "tiktok",
                "localField": "_id",
                "foreignField": "id_social",
                "as": "tiktok_list",
            }
        },
        {
            "$project": {
                "post_list": {
                    "$concatArrays": [
                        "$facebook_list",
                        "$twitter_list",
                        "$tiktok_list",
                    ],
                },
            },
        },
        {"$unwind": "$post_list"},
        {
            "$group": {
                "_id": {"$substr": ["$post_list.created_at", 0, 10]},
                "total_like": {"$sum": {"$toInt": "$post_list.like"}},
                "total_share": {"$sum": {"$toInt": "$post_list.share"}},
            }
        },
        {"$sort": {"_id": -1}},
    ]

    data = await client.aggregate(pipeline).to_list(None)
    return data


async def total_interaction_priority(id_social: str, start_date: str, end_date: str):
    filter_spec = {}

    # filter by start_date, end_date, text_search
    if start_date:
        start_date = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )
        start_date = str(start_date).replace("-", "/")

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_date = end_date.replace(hour=23, minute=59, second=59)
        end_date = str(end_date).replace("-", "/")

    if start_date != "" and end_date != "":
        filter_spec.update({"created_at": {"$gte": start_date, "$lte": end_date}})

    elif start_date != "":
        filter_spec.update({"created_at": {"$gte": start_date}})

    elif end_date != "":
        filter_spec.update({"created_at": {"$lte": end_date}})

    filter_spec.update({"id_social": ObjectId(id_social)})

    pipeline = [
        {"$match": {"_id": ObjectId(id_social)}},
        {
            "$lookup": {
                "from": "facebook",
                "pipeline": [{"$match": filter_spec}],
                "as": "facebook_list",
            }
        },
        {
            "$lookup": {
                "from": "twitter",
                "pipeline": [{"$match": filter_spec}],
                "as": "twitter_list",
            }
        },
        {
            "$lookup": {
                "from": "tiktok",
                "pipeline": [{"$match": filter_spec}],
                "as": "tiktok_list",
            }
        },
        {
            "$project": {
                "post_list": {
                    "$concatArrays": [
                        "$facebook_list",
                        "$twitter_list",
                        "$tiktok_list",
                    ],
                },
            },
        },
        {"$unwind": "$post_list"},
        {
            "$group": {
                "_id": "null",
                "total": {
                    "$sum": {
                        "$add": [
                            {"$ifNull": [{"$toInt": "$post_list.like"}, 0]},
                            {"$ifNull": [{"$toInt": "$post_list.comments"}, 0]},
                            {"$ifNull": [{"$toInt": "$post_list.share"}, 0]},
                        ],
                    }
                },
            }
        },
        {"$project": {"_id": 0, "total": 1}},
    ]

    data = await client.aggregate(pipeline).to_list(None)
    return data[0] if len(data) > 0 else []


async def total_post_priority(id_social: str, start_date: str, end_date: str):
    filter_spec = {}

    # filter by start_date, end_date, text_search
    if start_date:
        start_date = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )
        start_date = str(start_date).replace("-", "/")

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_date = end_date.replace(hour=23, minute=59, second=59)
        end_date = str(end_date).replace("-", "/")

    if start_date != "" and end_date != "":
        filter_spec.update({"created_at": {"$gte": start_date, "$lte": end_date}})

    elif start_date != "":
        filter_spec.update({"created_at": {"$gte": start_date}})

    elif end_date != "":
        filter_spec.update({"created_at": {"$lte": end_date}})

    filter_spec.update({"id_social": ObjectId(id_social)})

    pipeline = [
        {"$match": {"_id": ObjectId(id_social)}},
        {
            "$lookup": {
                "from": "facebook",
                "pipeline": [{"$match": filter_spec}],
                "as": "facebook_list",
            }
        },
        {
            "$lookup": {
                "from": "twitter",
                "pipeline": [{"$match": filter_spec}],
                "as": "twitter_list",
            }
        },
        {
            "$lookup": {
                "from": "tiktok",
                "pipeline": [{"$match": filter_spec}],
                "as": "tiktok_list",
            }
        },
        {
            "$project": {
                "post_list": {
                    "$concatArrays": [
                        "$facebook_list",
                        "$twitter_list",
                        "$tiktok_list",
                    ],
                },
            },
        },
        {"$addFields": {"total": {"$size": "$post_list"}}},
        {"$project": {"_id": 0, "post_list": 0}},
    ]

    data = await client.aggregate(pipeline).to_list(None)
    return data[0] if len(data) > 0 else []
