from vosint_ingestion.models import MongoRepository
from typing import *
from .models import Subject
from bson.objectid import ObjectId
import traceback

def get_my_subjects(text_search:str, page_size:int, page_index:int, user_id:str)->List[Any]:
    user = MongoRepository().get_one("users", {"_id": ObjectId(user_id)})
    subject_following = [] if user.get("subject_ids") is None else  user.get("subject_ids")
    user_subject_filter = {"_id": {"$in": [ObjectId(x) for x in subject_following]}}
    try:
        skip = page_size*(page_index-1)
        search_params = {
            "collection_name": "subjects",
            "filter_spec": user_subject_filter, 
            "pagination": {
                "skip": skip,
                "limit": page_size
            },
            "order": "sort_order",
        }

        if text_search not in [None, ""]:
            search_params["filter_spec"]["name"] = {"$regex": text_search, "$options": "i"}
        
        result, total_docs = MongoRepository().find(**search_params)
        for line in result:
            line["_id"] = str(line["_id"])

        return { "data": result, "total_records": total_docs }
    except Exception as e:
        traceback.print_exc()
        raise e

def get_subjects(text_search:str, page_size:int, page_index:int)->List[Any]:
    try:
        skip = page_size*(page_index-1)
        search_params = {
            "collection_name": "subjects",
            "filter_spec": {}, 
            "pagination": {
                "skip": skip,
                "limit": page_size
            },
            "order": "sort_order",
        }

        if text_search not in [None, ""]:
            search_params["filter_spec"]["name"] = {"$regex": text_search, "$options": "i"}
        
        result, total_docs = MongoRepository().find(**search_params)
        for line in result:
            line["_id"] = str(line["_id"])

        return { "data": result, "total_records": total_docs }
    except Exception as e:
        traceback.print_exc()
        raise e

def get_subject(subject_id:str)->Any:
    try:
        result, _ = MongoRepository().find("subjects", filter_spec={"_id": ObjectId(subject_id)})
        if len(result) == 0:
            raise Exception(f"subject {subject_id} no found")

        result[0]["_id"] = str(result[0]["_id"])
        return result[0]
    except Exception as e:
        traceback.print_exc()
        raise e
    
def delete_subjects(subject_ids:list[str])->Any:
    try:
        del_condition = [ObjectId(x) for x in subject_ids]
        del_count = 0
        if len(del_condition) > 0:
            del_count = MongoRepository().delete_many("subjects", filter_spec={"_id": {"$in": del_condition}})
        return del_count
    except Exception as e:
        traceback.print_exc()
        raise e

def update_subject(subject_id:str, update_val:dict[str, Any])->Any:
    try:
        update_count = 0
        if update_val.get("sub_id"):
            update_val.pop("sub_id")
        update_params = {
            "collection_name": "subjects",
            "filter_spec": {
                "_id": ObjectId(subject_id)
            },
            "action": {
                "$set": update_val
            }
        }
        update_count = MongoRepository().update_many(**update_params)
        return update_count
    except Exception as e:
        traceback.print_exc()
        raise e

def insert_subject(doc:dict[Any])->Any:
    try:
        if doc.get("sub_id"):
            doc.pop("sub_id")
        inserted_id = MongoRepository().insert_one("subjects", doc)
        return inserted_id
    except Exception as e:
        traceback.print_exc()
        raise e
    
def follow_subject(subject_id:str, user_id:str):
    update_params = {
        "collection_name": "users",
        "filter_spec": {
            "_id": ObjectId(user_id)
        },
        "action": {
            "$addToSet": {
                "subject_ids": subject_id
            }
        }
    }
    try:
        result =  MongoRepository().update_many(**update_params)
        return result
    except Exception as e:
        traceback.print_exc()
        raise e
    
def unfollow_subject(subject_id:str, user_id:str):
    update_params = {
        "collection_name": "users",
        "filter_spec": {
            "_id": ObjectId(user_id)
        },
        "action": {
            "$pull": {
                "subject_ids": subject_id
            }
        }
    }
    try:
        result =  MongoRepository().update_many(**update_params)
        return result
    except Exception as e:
        traceback.print_exc()
        raise e