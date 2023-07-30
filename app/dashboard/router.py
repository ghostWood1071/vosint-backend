from datetime import datetime, timedelta
from fastapi import APIRouter
from db.init_db import get_collection_client

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
