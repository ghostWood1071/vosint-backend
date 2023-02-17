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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    verified, updated_password_hash = verify_and_update(
        body.password, user["hashed_password"]
    )

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    # Update password has to a more robust one if needed
    if updated_password_hash is not None:
        await update_user(user["_id"], {"hashed_password": user["hashed_password"]})

    access_token = authorize.create_access_token(subject=str(user["_id"]))
    refresh_token = authorize.create_refresh_token(subject=str(user["_id"]))

    role = user["role"] if "role" in user else None

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return HTTPException(status_code=status.HTTP_200_OK, detail={"role": role})


@router.post("/refresh")
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)

    authorize.set_access_cookies(new_access_token)
    return HTTPException(status_code=status.HTTP_200_OK)


@router.delete("/logout")
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    authorize.unset_jwt_cookies()
    return HTTPException(status_code=status.HTTP_200_OK)
