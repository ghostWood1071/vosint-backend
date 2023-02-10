from fastapi import APIRouter, HTTPException
# from fastapi.security import HTTPBearer
# from fastapi_jwt_auth import AuthJWT
from app.user.models import UserCreate
from db.init_db import get_collection_client
from app.auth.password import get_password_hash

router = APIRouter()
"""
    Required Authorization
"""


@router.post("")
async def add(user_create: UserCreate):
    client = await get_collection_client("users")

    # TODO: validate password

    existing_user = await client.find_one({"username": user_create.username})
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    # user_dict = user_create.dict()
    # password = user_dict.pop("password")
    # user_dict["hashed_password"] = get_password_hash(password)
    # created_user = await client.insert_one(user_dict)

    # return created_user
