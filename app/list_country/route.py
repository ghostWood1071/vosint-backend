from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.list_country.model import CreateCountry, UpdateCountry
from app.list_country.service import (
    create_country,
    delete_country,
    get_all_country,
    get_one_country,
    update_country,
)
from db.init_db import get_collection_client

router = APIRouter()

db = get_collection_client("country")


@router.post("/")
async def add_country(payload: CreateCountry):
    country = payload.dict()
    exist_country = await db.find_one({"name": country["name"]})
    if exist_country:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="country already exist"
        )
    new_country = await create_country(country)
    return new_country


@router.get("/")
async def get_all():
    countries = await get_all_country()
    if countries:
        return countries
    return []


@router.get("/{name}")
async def get_one(name):
    country = await get_one_country(name)
    if country:
        return country
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="country not exist"
    )


@router.put("/{id}")
async def update_one(id, data: UpdateCountry = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_country = await update_country(id, data)
    if updated_country:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


@router.delete("/{id}")
async def delete_one(id):
    deleted_country = await delete_country(id)
    if deleted_country:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
