from fastapi import APIRouter
from typing import *
from .models import Action
from .services import *
import traceback
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.params import Depends
from db.init_db import get_collection_client

router = APIRouter()

@router.get("/get-actions")
def route_get_actions(search_text:str="", page_size:int=10, page_index:int=1, function_id:str="")->Any:
    try: 
        data = get_actions(search_text, page_size, page_index, function_id)
        
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.get("/get-action-by-id")
def route_get_action_by_id(action_id:str)->Action:
    try: 
        data = get_action(action_id)
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.post("/insert-action")
def route_insert_action(action: Action)->str:
    try: 
        data = insert_action(action.dict())
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.post("/update-action")
def route_update_action(action: Action)->int:
    try: 
        data = update_action(action.action_id, action.dict())
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.post("/delete-action")
def route_delete_action(action_ids:list[str])->int:
    try: 
        data = delete_actions(action_ids)
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.get("/get-actions-by-user")
async def route_get_actions_by_user(function_id: str, authorize: AuthJWT = Depends())->Any:
    try:
        user_collection = get_collection_client("users")
        role_collection = get_collection_client("role")
        authorize.jwt_required()

        user_id = authorize.get_jwt_subject()
        user = await user_collection.find_one({"_id": ObjectId(user_id)})

        role = await role_collection.find_one({
            "$or": [
                {"_id": ObjectId(user.get("role_id"))},
                {"role_code": user.get("role")}
            ]
        })

        role_function_collection = get_collection_client("role_function")

        role_function = await role_function_collection.find_one({
            "$and": [
                {"function_id": str(function_id)},
                {"role_id": str(role["_id"])}
            ]
        })

        data = await get_actions_by_user(function_id, role_function.get("_id"))
        
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))
