from fastapi import HTTPException, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

from pydantic import BaseModel

from core.logging import logger

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    logger.info('Login Request: ' + user.username)
    if user.username != "test" or user.password != "test":
        logger.error('Login Failed')
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


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
