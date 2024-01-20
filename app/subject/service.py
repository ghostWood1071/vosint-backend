from vosint_ingestion.models import MongoRepository
from typing import *
from .models import Subject
from bson.objectid import ObjectId
import traceback

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
            "order": "sort_order"
        }
        if text_search not in [None, ""]:
            search_params["name"] = {
                "$regex": text_search
            }
        
        
        result = MongoRepository().find(**search_params)
        for line in result:
            line["_id"] = str(line["_id"])
        return result 
    except Exception as e:
        traceback.print_exc()
        raise e

def get_subject(subject_id:str)->Any:
    try:
        result = MongoRepository().find("subjects", filter_spec={"_id": ObjectId(subject_id)})
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