from bson.objectid import ObjectId
from fastapi import HTTPException, status

from db.init_db import get_collection_client

infor_collect = get_collection_client("infor")


async def create_infor(infor):
    created = await infor_collect.insert_one(infor)
    new = await infor_collect.find_one({"id": created.inserted_id})
    return HTTPException(status_code=status.HTTP_200_OK, detail="OK")


async def get_all_infor():
    list_infor = []
    async for item in infor_collect.find():
        list_infor.append(Entity(item))
    return list_infor


async def search_infor(keyword: str) -> dict:
    infor = await infor_collect.find_one(
        {"$or": [{"infor_name": keyword}, {"host_name": keyword}]}
    )
    if infor:
        return Entity(infor)


async def update_infor(id: str, data: dict):
    infor = await infor_collect.find_one({"_id": ObjectId(id)})
    if infor:
        updated_infor = await infor_collect.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_infor:
            return status.HTTP_200_OK
        return False


async def delete_infor(id: str):
    infor = await infor_collect.find_one({"_id": ObjectId(id)})
    if infor:
        await infor_collect.delete_one({"_id": ObjectId(id)})
        return True


def Entity(infor) -> dict:
    return {
        "_id": str(infor["_id"]),
        "infor_name": infor["infor_name"],
        "host_name": infor["host_name"],
        "language": infor["language"],
        "publishing_country": infor["publishing_country"],
        "source_type": infor["source_type"],
    }
