from datetime import datetime, timedelta

from fastapi import APIRouter

from db.init_db import get_collection_client

from .service import (
    count_news_country_today,
    count_news_hours,
    news_country_today,
    news_hours_today,
)

router = APIRouter()

client_events = get_collection_client("events")


@router.get("/hot-news-today")
async def get_hot_news_today():
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1, seconds=-1)

    pipeline = [
        {
            "$match": {
                "date_created": {
                    "$gte": start_of_day,
                    "$lt": end_of_day,
                }
            }
        },
        {
            "$project": {
                "new_list_length": {"$size": "$new_list"},
                "event_content": 1,
                "event_name": 1,
                "chu_the": 1,
                "khach_the": 1,
                "date_created": 1,
            }
        },
        {"$sort": {"new_list_length": -1}},
        {"$limit": 10},
    ]
    result = await client_events.aggregate(pipeline).to_list(None)
    return {"result": result}


@router.get("/news-country-today")
async def get_news_country_today(start_day: int):
    return await news_country_today(start_day)


@router.get("/news-hours-today")
async def get_news_hours_today():
    return await news_hours_today()


@router.post("/count-news-country-today")
async def get_count_news_country_today():
    return await count_news_country_today()


@router.post("/count-news-hours")
async def get_count_news_hours():
    return await count_news_hours()
