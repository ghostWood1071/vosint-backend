from datetime import datetime

from db.init_db import get_collection_client

client = get_collection_client("News_vnanet")

async def get_all(text_search, start, end, check, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    query = {}
    list_craw = []
    if text_search:
        query = {"title": {"$regex": text_search, "$options": "i"}}
    if start and end:
        start_date = datetime.strptime(start, "%d/%m/%Y")
        end_date = datetime.strptime(end, "%d/%m/%Y")
        query = {"date": {"$gte": start_date, "$lte": end_date}}
    if check:
        query = {"is_crawled": check}
    if not query:
        query = {}
    async for item in client.find(query).sort("_id").skip(offset).limit(limit): 
        list_craw.append(item)
    return list_craw
        