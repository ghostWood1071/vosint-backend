from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.list_object.model import CreateObject, UpdateObject
from db.init_db import get_collection_client
from app.list_object.service import create_object, update_object, get_all_object, get_one_object, delete_object

router = APIRouter()

db = get_collection_client("object")

@router.post("/")
async def add_object(payload: CreateObject):
    object = payload.dict()
    exist_object = await db.find_one({'object_name': object['object_name']}) 
    if exist_object:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='object already exist')
    new_object = await create_object(object)
    return new_object

@router.get("/")
async def get_all():
    countries = await get_all_object()
    if countries:
        return countries
    return []

@router.get("/{id}")
async def get_one(id):
    object = await get_one_object(id)
    if object:
        return object
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='object not exist')

@router.put("/{id}")
async def update_one(id, data: UpdateObject = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_object = await update_object(id, data)
    if updated_object:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN

@router.delete("/{id}")
async def delete_one(id):
    deleted_object = await delete_object(id)
    if deleted_object:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
    