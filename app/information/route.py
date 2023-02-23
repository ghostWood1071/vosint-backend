from fastapi import APIRouter, Body, HTTPException, status

from app.information.model import CreateInfor, UpdateInfor
from app.information.service import (
    create_infor,
    delete_infor,
    get_all_infor,
    search_infor,
    update_infor,
)
from db.init_db import get_collection_client

router = APIRouter()
infor_collect = get_collection_client("infor")

@router.post("/")
async def add_infor(payload: CreateInfor):
    infor = payload.dict()
    exist_infor = await infor_collect.find_one({"infor_name": infor["infor_name"]})
    if exist_infor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="infor already exist"
        )
    new_infor = await create_infor(infor)
    return new_infor

@router.get("/")
async def get_all():
    list_infor = await get_all_infor()
    if list_infor: 
        return list_infor
    return None

@router.get("/{name}")
async def search(name):
    infor = await search_infor(name)
    
    if name == infor["infor_name"]:
        return {
            "message": "Your search math the name",
            "result": infor
        }
        
    if name == infor["host_name"]:
        return {
            "message": "Your search math the host name",
            "result": infor
        }
        
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="infor not exist"
    )
    
@router.put("/{id}")
async def update(id, data: UpdateInfor = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_infor = await update_infor(id, data)
    if updated_infor:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN

@router.delete("/{id}")
async def delete(id):
    deleted_infor = await delete_infor(id)
    if deleted_infor:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
