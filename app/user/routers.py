from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.auth.password import get_password_hash
# from fastapi.security import HTTPBearer
# from fastapi_jwt_auth import AuthJWT
from app.user.models import UserCreateModel
from app.user.services import create_user, get_all_user, get_user
from db.init_db import get_collection_client

router = APIRouter()
"""
    Required Authorization
"""

client = get_collection_client("users")


@router.post("/")
async def add(body: UserCreateModel):
    user_dict = body.dict()

    existing_user = await client.find_one({'username': user_dict['username']})

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User already exist')

    user_dict['hashed_password'] = get_password_hash(user_dict['password'])
    user_dict.pop("password")
    created_user = await create_user(user_dict)
    print(created_user)

    # return user_dict
    # user_create.password = user_create.password
    # user = jsonable_encoder(user_create)
    # new_user = await add_user(user)
    # return new_user


@router.get("/")
async def get_all():
    users = await get_all_user()
    if users:
        return users
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail='List of account users is empty')


@router.get('/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user_id(id):
    user = await get_user(id)
    if user:
        return user
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail='user not exist')


# @router.put('/{id}', dependencies=[Depends(HTTPBearer())])
# async def update_user(id: str, user_data: UserUpdateModel = Body(...)):
#     user_data = {k: v for k, v in user_data.dict().items() if v is not None}
#     updated_user = await update_user(id, user_data)
#     if updated_user:
#         return updated_user
#     return status.HTTP_403_FORBIDDEN
#

# @router.delete('/{id}', dependencies=[Depends(HTTPBearer())])
# async def delete_user(id: str):
#     deleted_user = await delete_user(id)
#     if deleted_user:
#         return status.HTTP_200_OK
#     return status.HTTP_403_FORBIDDEN
