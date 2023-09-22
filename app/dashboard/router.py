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
    status_source_news,
    source_news_lowest_hightest,
    users_online,
    top_country_by_entities,
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
# ------- Start leader --------
@router.get("/get-news-seven-nearest")
async def get_news_seven_nearest_r(day_space: int = 7):
    return await news_seven_nearest(day_space)


@router.get("/get-top-news-by-topic")
async def get_top_news_by_topic(day_space: int = 7):
    return await top_news_by_topic(day_space)


@router.get("/get-top-news-by-country")
async def get_top_news_by_country(day_space: int = 7, top: int = 5):
    return await top_country_by_entities(day_space, top)


@router.get("/get-total-users")
async def get_total_users():
    return await total_users()


@router.get("/get-total-users-online")
async def get_total_users_online():
    return await users_online()


@router.get("/get-top-user-read")
async def get_top_user_read(top: int = 5):
    return await top_user_read(top)


# ------- End leader --------


# ------- Start expert --------
@router.get("/get-source-news-lowest-hightest")
async def get_source_news_lowest_hightest():
    return await source_news_lowest_hightest()


# ------- End expert --------


# ------- Start admin --------
@router.get("/get-status-source-news")
async def get_status_source_news(day_space: int = 7):
    return await status_source_news(day_space)


# ------- End admin --------
