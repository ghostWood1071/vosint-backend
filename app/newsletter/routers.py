from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from app.newsletter.utils import newsletter_to_object_id

from .models import NewsLetterCreateModel, NewsLetterUpdateModel
from .services import create_newsletter, delete_newsletter, find_newsletters_and_filter, update_newsletter

router = APIRouter()


@router.post("/", dependencies=[Depends(HTTPBearer())])
async def create(body: NewsLetterCreateModel, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    newsletter_dict = body.dict()
    newsletter_dict["user_id"] = user_id
    await create_newsletter(newsletter_to_object_id(newsletter_dict))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)


@router.get("/", dependencies=[Depends(HTTPBearer())])
async def read(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    newsletters = await find_newsletters_and_filter({"user_id": ObjectId(user_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content=newsletters)


@router.delete("/{newsletter_id}", dependencies=[Depends(HTTPBearer())])
async def delete(newsletter_id: str):
    await delete_newsletter(ObjectId(newsletter_id))
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.patch("/{newsletter_id}", dependencies=[Depends(HTTPBearer())])
async def update(newsletter_id: str, body: NewsLetterUpdateModel):
    parsed_newsletter = newsletter_to_object_id(body.dict())
    await update_newsletter(ObjectId(newsletter_id), parsed_newsletter)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
