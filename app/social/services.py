from typing import List

from bson import ObjectId
from fastapi import status

from app.social.models import AddFollow, UpdateAccountMonitor
from db.init_db import get_collection_client

client = get_collection_client("socials")
client2 = get_collection_client("social_media")


async def get_all_user(skip, limit):
    users = []
    async for user in client.find().limit(limit).skip(limit * skip):
        users.append(user_entity(user))
    return users


async def get_user(id: str) -> dict:
    users = await client.find_one({"_id": ObjectId(id)})
    if users:
        return user_entity(users)


async def create_user(user):
    created_user = await client.insert_one(user)
    new_user_id = str(created_user.inserted_id)
    filter_result = await client.find_one({"_id": ObjectId(new_user_id)})
    username = filter_result["username"]
    # update the followed_by list for each followed
    followeds = user.get("users_follow", [])
    await client2.update_many(
        {
            "_id": {
                "$in": [ObjectId(followed.get("follow_id")) for followed in followeds]
            }
        },
        {
            "$push": {
                "followed_by": {
                    "followed_id": new_user_id,
                    "username": username,
                }
            }
        },
    )
    return await client.find_one({"id": created_user.inserted_id})


async def delete_user(id: str):
    str_id = str(id)
    user = await client.find_one({"_id": ObjectId(id)})
    username = user["username"]
    followeds = []
    filter_object = user.get("users_follow")
    for filter_list in filter_object:
        followeds.append(
            {
                "follow_id": str(filter_list.get("follow_id")),
                "social_name": str(filter_list.get("social_name")),
            }
        )
    await client2.update_many(
        {"_id": {"$in": [ObjectId(f["follow_id"]) for f in followeds]}},
        {
            "$pull": {
                "followed_by": {
                    "followed_id": str_id,
                    "username": username,
                }
            }
        },
    )
    if user:
        await client.delete_one({"_id": ObjectId(id)})
        return True


async def update_username_user(id: str, username_new: str):
    user = await client.find_one({"_id": ObjectId(id)})
    user_id = str(id)
    followeds = user.get("users_follow", [])
    await client2.update_many(
        {"_id": {"$in": [ObjectId(followed["follow_id"]) for followed in followeds]}},
        {"$set": {f"followed_by.$[elem].username": username_new}},
        array_filters=[{"elem.followed_id": user_id}],
    )
    if user:
        await client.update_one(
            {"_id": ObjectId(id)}, {"$set": {"username": username_new}}
        )
        return True
    return False


async def update_follow_user(id: str, data: List[AddFollow]):
    user_id = str(id)
    filter_result = await client.find_one({"_id": ObjectId(id)})
    username = filter_result["username"]
    followeds = []
    for datum in data:
        followeds.append(
            {"follow_id": datum.follow_id, "social_name": datum.social_name}
        )
    await client2.update_many(
        {"_id": {"$in": [ObjectId(f["follow_id"]) for f in followeds]}},
        {"$addToSet": {"followed_by": {"followed_id": user_id, "username": username}}},
    )

    return await client.update_one(
        {"_id": ObjectId(id)},
        {"$addToSet": {"users_follow": {"$each": [datum.dict() for datum in data]}}},
    )


async def delete_follow_user(id: ObjectId, data: List[AddFollow]):
    user_id = str(id)
    filter_result = await client.find_one({"_id": ObjectId(id)})
    username = filter_result["username"]
    followeds = []
    for datum in data:
        followeds.append(
            {
                "follow_id": str(datum.follow_id),
                "social_name": datum.social_name,
            }
        )
    await client2.update_many(
        {"_id": {"$in": [ObjectId(f["follow_id"]) for f in followeds]}},
        {
            "$pull": {
                "followed_by": [
                    {
                        "followed_id": user_id,
                        "username": username,
                    }
                ]
            }
        },
    )
    docs = [dict(datum) for datum in data]
    return await client.update_one(
        {"_id": id}, {"$pull": {"users_follow": {"$in": docs}}}
    )


async def update_account_monitor(data: UpdateAccountMonitor):
    _id = data["id"]
    user_id = str(_id)
    socials = await client.find_one({"_id": ObjectId(_id)})
    username = socials["username"]
    compare_name = data["username"]
    if username == compare_name:
        username = username
    elif username != compare_name:
        username = compare_name
    users_follow = data.get("users_follow", [])

    await client2.update_many(
        {
            "followed_by.followed_id": user_id,
            "followed_by.username": username,
        },
        {
            "$pull": {
                "followed_by": {
                    "followed_id": user_id,
                    "username": username,
                }
            }
        },
    )

    for user_follow in users_follow:
        user_follow_id = user_follow.get("follow_id")
        await client2.update_one(
            {"_id": ObjectId(user_follow_id)},
            {
                "$addToSet": {
                    "followed_by": {
                        "followed_id": user_id,
                        "username": username,
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


async def get_account_monitor_by_media(
    social_media: str, page: int = 1, limit: int = 20
):
    offset = (page - 1) * limit if page > 0 else 0
    list_social_media = []
    async for item in client.find(social_media).sort("_id").skip(offset).limit(limit):
        item = To_json(item)
        list_social_media.append(user_entity(item))
    return list_social_media


def To_json(media) -> dict:
    media["_id"] = str(media["_id"])
    return media


async def count_object(filter_object):
    return await client.count_documents(filter_object)


def user_entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"],
        "social": user["social"],
        "users_follow": user["users_follow"],
        "list_proxy": user["list_proxy"],
    }
