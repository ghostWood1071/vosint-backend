from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.newsletter.utils import newsletter_to_json, newsletter_to_ojbectId

from .models import NewsLetterCreateModel, NewsLetterUpdateModel
from .services import create_newsletter, delete_newsletter, find_newsletter_by_id, find_newsletters_by_user_id, update_newsletter

router = APIRouter()


@router.post("/")
async def create(body: NewsLetterCreateModel):
    parsed_newsletter = newsletter_to_ojbectId(body.dict())
    created_newsletter = await create_newsletter(parsed_newsletter)
    created_newsletter = await find_newsletter_by_id(
        created_newsletter.inserted_id)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=newsletter_to_json(created_newsletter))


@router.get("/")
async def read_by_user_id(user_id: str, skip=0, limit=20):
    newsletters = await find_newsletters_by_user_id(user_id, int(skip),
                                                    int(limit))
    return JSONResponse(status_code=status.HTTP_200_OK, content=newsletters)


@router.delete("/{newsletter_id}")
async def delete(newsletter_id: str):
    await delete_newsletter(ObjectId(newsletter_id))
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.patch("/{newsletter_id}")
async def update(newsletter_id: str, body: NewsLetterUpdateModel):
    parsed_newsletter = newsletter_to_ojbectId(body.dict())
    await update_newsletter(ObjectId(newsletter_id), parsed_newsletter)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
