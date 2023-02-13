from fastapi import HTTPException, Depends, APIRouter, Body
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from app.auth.auth_handler import signJWT
from pydantic import BaseModel
from db.init_db import get_collection_client
from core.logging import logger
from app.auth.password import get_password_hash

router = APIRouter()

client = get_collection_client("users")
class User(BaseModel):
    username: str
    password: str

async def check_user(data: User):
    result = await client.find_one({"username": data.username})
    if (result['password']) == data.password:
        result.pop('password')
        result.pop('fullname')
        result.pop('account_type')
        result["id"]=str(result["_id"])
        del result["_id"]
        return result
    return None


@router.post('/login')
# async def login(user: User, Authorize: AuthJWT = Depends()):
#     logger.info('Login Request: ' + user.username)
#     if user.username != "test" or user.password != "test":
#         logger.error('Login Failed')
#         raise HTTPException(status_code=401, detail="Bad username or password")

#     access_token = Authorize.create_access_token(subject=user.username)
#     refresh_token = Authorize.create_refresh_token(subject=user.username)
#     return {"access_token": access_token, "refresh_token": refresh_token}

async def user_login(user: User = Body(...)):
    find = await client.find_one({"username": user.username})
    if not find:
        return { "error": "Account not exist"}
    user = await check_user(user)
    if user:
        return signJWT(user)
    return { "error": "Invalid Login Account" }


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    return {"access_token": new_access_token}


@router.get('/protected', dependencies=[Depends(HTTPBearer())])
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    return {"user": current_user}
