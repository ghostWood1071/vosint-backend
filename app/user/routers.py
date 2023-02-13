from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.encoders import jsonable_encoder
# from fastapi.security import HTTPBearer
# from fastapi_jwt_auth import AuthJWT
from app.user.models import UserCreate, UpdateUser
from db.init_db import get_collection_client
from app.auth.password import get_password_hash
from app.user.service import add_user, get_all_user, get_user, Update_user, Delete_user
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer


router = APIRouter()
"""
    Required Authorization
"""

client = get_collection_client("users")


@router.post("/", status_code = status.HTTP_200_OK, response_model = UserCreate, dependencies=[Depends(HTTPBearer())])
async def add(user_create: UserCreate):
    existing_user = await client.find_one({'username': user_create.username.lower()})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = 'User already exist')
    
    user_create.password = user_create.password
    user = jsonable_encoder(user_create)
    new_user = await add_user(user)
    return new_user

@router.get("/", dependencies=[Depends(HTTPBearer())])
async def get_all():
    users = await get_all_user()
    if users:
        return users
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'List of account users is empty')

@router.get('/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user_id(id):
    user = await get_user(id)
    if user:
        return user
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'user not exist')

@router.put('/{id}', dependencies=[Depends(HTTPBearer())])
async def update_user(id: str, user_data: UpdateUser = Body(...)):
    user_data = {
        k: v for k,
        v in user_data.dict().items() if v is not None
    }
    updated_user = await Update_user(id, user_data)
    if updated_user:
        return updated_user
    return status.HTTP_403_FORBIDDEN

@router.delete('/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_user(id: str):
    deleted_user = await Delete_user(id)
    if deleted_user:
        return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN
    
