from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from app.auth.password import verify_and_update

from app.user.models import UserLoginModel
from app.user.services import read_user_by_username, update_user

router = APIRouter()


@router.post("/login")
async def login(body: UserLoginModel, authorize: AuthJWT = Depends()):
    user = await read_user_by_username(body.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Username or password is valid")

    verified, updated_password_hash = verify_and_update(
        body.password, user["hashed_password"])

    if not verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Username or password is valid")

    # Update password has to a more robust one if needed
    if updated_password_hash is not None:
        await update_user(user["_id"],
                          {"hashed_password": user["hashed_password"]})

    access_token = authorize.create_access_token(subject=str(user["_id"]))
    refresh_token = authorize.create_refresh_token(subject=str(user["_id"]))
    role = user["role"] if "role" in user else None;

    return HTTPException(status_code=status.HTTP_201_CREATED,
                         detail={"access_token": access_token, "refresh_token": refresh_token, "role": role})
