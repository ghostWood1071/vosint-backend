from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status

from app.list_organize.model import CreateOrganize, UpdateOrganize
from app.list_organize.service import (
    create_organize,
    delete_organize,
    get_all_organize,
    get_one_organize,
    update_organize,
)
from db.init_db import get_collection_client

router = APIRouter()

db = get_collection_client("organize")

@router.post("/")
async def add_organize(payload: CreateOrganize):
    organize = payload.dict()
    exist_organize = await db.find_one({'organize_name': organize['organize_name']}) 
    if exist_organize:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Organize already exist')
    new_organize = await create_organize(organize)
    return new_organize

@router.get("/")
async def get_all():
    organizes = await get_all_organize()
    if organizes:
        return organizes
    return []

@router.get("/{name}")
async def get_one(name):
    organize = await get_one_organize(name)
    if organize:
        return organize
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Organize not exist')

@router.put("/{id}")
async def update_one(id, data: UpdateOrganize = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_organize = await update_organize(id, data)
    if updated_organize:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN

@router.delete("/{id}")
async def delete_one(id):
    deleted_organize = await delete_organize(id)
    if deleted_organize:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
    