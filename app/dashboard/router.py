from datetime import datetime, timedelta

from fastapi import APIRouter

from .service import (
    count_news_country_today,
    count_news_hours,
    news_country_today,
    news_hours_today,
    news_seven_nearest,
    top_news_by_topic,
    top_news_by_country,
    top_user_read,
    total_users,
    hot_events_today,
)

router = APIRouter()


@router.get("/hot-events-today")
async def get_hot_events_today():
    return await hot_events_today()


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


# New
@router.get("/get-news-seven-nearest")
async def get_news_seven_nearest_r():
    return await news_seven_nearest()


@router.get("/get-top-news-by-topic")
async def get_top_news_by_topic():
    return await top_news_by_topic()


@router.get("/get-top-news-by-country")
async def get_top_news_by_country():
    return await top_news_by_country()


@router.get("/get-total-users")
async def get_total_users():
    return await total_users()


@router.get("/get-top-user-read")
async def get_top_user_read():
    return await top_user_read()
