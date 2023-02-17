def news_to_json(news) -> dict:
    news["_id"] = str(news["_id"])

    return news
