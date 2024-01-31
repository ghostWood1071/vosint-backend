# import datetime
from datetime import datetime, timedelta
import json
from typing import *
from bson.objectid import ObjectId

from db.init_db import get_collection_client

from .utils import news_to_json
from vosint_ingestion.models import MongoRepository
from vosint_ingestion.features.elasticsearch.elastic_main import MyElasticSearch
from vosint_ingestion.features.job.services.get_news_from_elastic import (
    build_search_query_by_keyword,
    build_language
)
from app.newsletter.models import NewsletterTag
from core.config import settings
import nltk
from nltk.tokenize import word_tokenize
from langdetect import detect
from pyvi import ViTokenizer
import re
import jieba

client = get_collection_client("News")
news_es = MyElasticSearch()

all_punctuation = ['*', '%', '(', ')', '+', '[', '\\', '!', '@', '`', ']', '^', ',', '.', '/', '<', '=', '>', '?', '&', "'", '-', ':', ';', '_', '{', '|', '}', '~', '"', '#', '$']
punctuation_regex = re.compile(f"[{''.join(re.escape(char) for char in all_punctuation)}]")
nltk.download('punkt') 
lang_dict = {
    "vi": "vietnamese",
    "cn": "chinese",
    "en": "english",
    "ru": "russian"
}

async def find_news_by_filter(filter, projection=None):
    news = []
    async for new in client.find(filter, projection).sort("_id"):
        new = news_to_json(new)
        news.append(new)

    return news


async def find_news_by_filter_and_paginate(
    filter_news, projection, skip: int, limit: int
):
    offset = (skip - 1) * limit if skip > 0 else 0
    news = []
    async for new in client.find(filter_news, projection).sort("_id").skip(
        offset
    ).limit(limit):
        new = news_to_json(new)
        if "is_read" not in new:
            await client.aggregate([{"$addFields": {"is_read": False}}]).to_list(
                length=None
            )

        if "list_user_read" not in new:
            await client.aggregate([{"$addFields": {"list_user_read": []}}]).to_list(
                length=None
            )

        if "event_list" not in new:
            await client.aggregate([{"$addFields": {"event_list": []}}]).to_list(
                length=None
            )
        news.append(new)
    return news


async def count_news(filter_news):
    return await client.count_documents(filter_news)


async def find_news_by_id(news_id: ObjectId):
    # projection["pub_date"] = str(projection["pub_date"])
    # return await client.find_one({"_id": news_id}, projection)
    return await client.find_one({"_id": news_id})


async def read_by_id(news_ids: List[str], user_id: str):
    news_id_list = [ObjectId(news_id) for news_id in news_ids]
    return await client.update_many(
        {"_id": {"$in": news_id_list}, "list_user_read": {"$not": {"$all": [user_id]}}},
        {"$set": {"is_read": True}, "$push": {"list_user_read": user_id}},
    )


async def unread_news(new_ids: List[str], user_id: str):
    news_id_list = [ObjectId(row_new) for row_new in new_ids]
    news_filter = {"_id": {"$in": news_id_list}}
    return await client.update_many(
        news_filter, {"$pull": {"list_user_read": {"$in": [user_id]}}}
    )


async def find_news_by_ids(ids: List[str], projection: Dict["str", Any]):
    list_ids = []
    for index in ids:
        list_ids.append(ObjectId(index))
    news_list = []
    async for news in client.find({"_id": {"$in": list_ids}}, projection):
        news_list.append(news)
    return news_list

def get_check_news_contain_list(news_ids, keywords):
    object_filter = [ObjectId(object_id) for object_id in news_ids]
    news, _ = MongoRepository().get_many("News", {"_id": {"$in": object_filter}})
    for item in news:
        item["is_contain"] = False
        item["_id"] = str(item["_id"])
        item["pub_date"] = str(item["pub_date"])
        for keyword in keywords:
            if (
                keyword.lower() in item["data:title"].lower()
                or keyword.lower() in item["data:content"].lower()
                or keyword.lower() in item["keywords"]
            ):
                item["is_contain"] = True
                break
    return news

def check_news_contain_keywords(
    object_ids: List[str], news_ids: List[str], new_keywords: List[str] = []
):
    object_filter = [ObjectId(object_id) for object_id in object_ids]
    objects, _ = MongoRepository().get_many("object", {"_id": {"$in": object_filter}})
    keywords = []
    for object in objects:
        if object.get("keywords"):
            for keyword in list(object["keywords"].values()):
                item_key_words = [key.strip() for key in keyword.split(",")]
                keywords.extend(item_key_words)
    if len(new_keywords) > 0:
        keywords.extend(new_keywords)
    while "" in keywords:
        keywords.remove("")
    print(keywords)
    result = get_check_news_contain_list(news_ids, keywords)
    return result

def check_type_newsletters(newsletters:list[Any], type_name:str):
    if len(newsletters) == 0:
        return False
    checks = [newsletter.get("tag") == type_name for newsletter in newsletters]
    return all(checks)

async def lol(filter_spec):
    data = []
    async for line in client.find(filter_spec):
        data.append(line)
    return data

async def statistics_sentiments(filter_spec, params):
    news_letter_id = params.get("newsletter_id")
    text_search = params.get("text_search")
    newsletter_type = params.get("newsletter_type")
    all_selfs = None
    all_archives = None
    #--- build subject query --- 
    user =MongoRepository().get_one("users", {"_id" :ObjectId(params.get("user_id"))})
    user_lang = [] if user.get("languages") is None else user.get("languages")
    user_ignore_sources = [] if user.get("sources") is None else user.get("sources")
    if params.get("subject_id") is None:
        subject_ids = [] if user.get("subject_ids") is None else user.get("subject_ids")
        if filter_spec.get("$and") is None:
            filter_spec["$and"] = []
        filter_spec["$and"].append({
            "subject_id": {"$in": subject_ids}
        })
        subject_query = " | ".join([f'"{x}"' for x in subject_ids])
    else:
        if filter_spec.get("$and") is None:
            filter_spec["$and"] = []
        filter_spec["$and"].append({
            "subject_id":  params.get("subject_id")
        })
        subject_query = f'"{params.get("subject_id")}"'
    # --------------------------
    # --- build languages query ---
    language_source = params.get("language_source")
    language_source = build_language(user_lang, language_source) 
    if language_source is None:
        return {
            "total_positive": 0,
            "total_negative": 0,
            "total_normal": 0,
        }
    else:
        if filter_spec.get("$and") is None:
            filter_spec["$and"] = []
        filter_spec["$and"].append({
            "source_language": {"$in": language_source}
        })
    
    # ---------------------------
    # --- build ignore source query ---
    if len(user_ignore_sources) > 0:
        if filter_spec.get("$and") is None:
            filter_spec["$and"] = []
        filter_spec["$and"].append({
            "source_id": {"$nin": user_ignore_sources}
        })
         
    query = "*"
    news_ids = []
    if params.get("vital") == '1':
        vital_ids = [] if user.get("vital_list") is None else user.get("vital_list")
        if len(vital_ids) > 0: 
            if filter_spec.get("$and") is None:
                filter_spec["$and"] = []
            filter_spec["$and"].append({
                "_id": {"$in": vital_ids}
            })
            news_ids = [str(x) for x in vital_ids]
        else:
            return {
                "total_positive": 0,
                "total_negative": 0,
                "total_normal": 0,
            }
    
    if params.get("bookmarks") == '1':
        bookmarks_ids = [] if user.get("news_bookmarks") is None else user.get("news_bookmarks")
        bookmarks_filter = [str(x) for x in bookmarks_ids]
        if len(bookmarks_ids) > 0: 
            if filter_spec.get("$and") is None:
                filter_spec["$and"] = []
            filter_spec["$and"].append({
                "_id": {"$in": bookmarks_ids}
            })
            news_ids = bookmarks_filter
        else:
            return {
                "total_positive": 0,
                "total_negative": 0,
                "total_normal": 0,
            }

    if news_letter_id not in ["", None] or newsletter_type not in ["", None]:
        news_letter_filter = {"tag": newsletter_type} if newsletter_type not in ["", None] else {"_id": ObjectId(news_letter_id)}
        news_letter_filter["user_id"] = ObjectId(params.get("user_id"))
        news_letters, _ = MongoRepository().find(
            collection_name="newsletter", filter_spec=news_letter_filter
        )
        if len(news_letters) == 0:
            return {
                "total_positive": 0,
                "total_negative": 0,
                "total_normal": 0,
            }
        # nếu không là giỏ tin
        all_selfs = check_type_newsletters(news_letters, NewsletterTag.SELFS)
        if newsletter_type == NewsletterTag.SELFS or all_selfs:
            tmp_phrase_search = []
            for news_letter in news_letters:
                query_tmp = build_search_query_by_keyword(news_letter)
                if query_tmp not in [None, ""]:
                    tmp_phrase_search.append(f'({query_tmp})')
            if len(tmp_phrase_search) > 0:
                query = " | ".join(tmp_phrase_search)
        all_archives = check_type_newsletters(news_letters, NewsletterTag.ARCHIVE)
        if newsletter_type == NewsletterTag.ARCHIVE or all_archives:
            for newsletter in news_letters:
                if newsletter.get("news_id") is not None:
                    news_ids.extend(newsletter.get("news_id"))
            if text_search in ["", None]:
                if filter_spec.get("$and") is None:
                    filter_spec["$and"] = []
                filter_spec["$and"].append({
                    "_id": {"$in": news_ids}
                })
            else:
                news_ids = [str(x) for x in news_ids]
    
    if text_search not in [None, ""]:
        if query !=  "*":
            query = f'({query}) + ("{text_search}")'
        else:
            query = text_search
    
       
    if text_search not in ["", None] or all_selfs or newsletter_type == NewsletterTag.SELFS:
        total_docs = news_es.count_search_main(
            index_name=settings.ELASTIC_NEWS_INDEX,
            query=query,
            gte=params["start_date"],
            lte=params["end_date"],
            lang=params["language_source"],
            sentiment=params["sentiment"],
            subject_id=subject_query,
            list_id=news_ids,
            list_source_id=user_ignore_sources
        )

        total_positive = news_es.count_search_main(
            index_name=settings.ELASTIC_NEWS_INDEX,
            query=query,
            gte=params["start_date"],
            lte=params["end_date"],
            lang=params["language_source"],
            sentiment="1"
            if params["sentiment"] == "" or params["sentiment"] == "1"
            else 9999,
            subject_id = subject_query,
            list_id=news_ids,
            list_source_id=user_ignore_sources
        )

        total_negative = news_es.count_search_main(
            index_name=settings.ELASTIC_NEWS_INDEX,
            query=query,
            gte=params["start_date"],
            lte=params["end_date"],
            lang=params["language_source"],
            sentiment="2"
            if params["sentiment"] == "" or params["sentiment"] == "2"
            else 9999,
            subject_id = subject_query,
            list_id=news_ids,
            list_source_id=user_ignore_sources
        )

        total_normal = total_docs - (total_negative + total_positive)

    else:
        # Get total documents
        
        total_docs = await client.count_documents(filter_spec)
        xxx = await lol(filter_spec)
        # Get total sentiments
        check_array = filter_spec.get("$and") or []

        updated_conditions = []
        for condition in check_array:
            if "data:class_sacthai" in condition:
                removed_object = condition
            else:
                updated_conditions.append(condition)

        total_positive = await client.count_documents(
            {
                **filter_spec,
                **{"$and": [*updated_conditions, {"data:class_sacthai": "9999"}]},
            }
            if any(
                "data:class_sacthai" in obj and obj["data:class_sacthai"] != "1"
                for obj in check_array
            )
            else {
                **filter_spec,
                **{"$and": [*updated_conditions, {"data:class_sacthai": "1"}]},
            }
        )
        total_negative = await client.count_documents(
            {
                **filter_spec,
                **{"$and": [*updated_conditions, {"data:class_sacthai": "9999"}]},
            }
            if any(
                "data:class_sacthai" in obj and obj["data:class_sacthai"] != "2"
                for obj in check_array
            )
            else {
                **filter_spec,
                **{"$and": [*updated_conditions, {"data:class_sacthai": "2"}]},
            }
        )
        total_normal = total_docs - (total_positive + total_negative)

    total_sentiments = {
        "total_positive": total_positive,
        "total_negative": total_negative,
        "total_normal": total_normal,
    }

    return {"total_records": total_docs, "total_sentiments": total_sentiments}


async def collect_keyword(subject_name:str, keyword:Any, user_id:str, collect_time:str):
    search_client = get_collection_client("search_history")
    collected_time = datetime.strptime(collect_time, "%d/%m/%Y %H:%M:%S")
    words = []
    try:
        keyword = eval(keyword)
    except Exception as e:
        pass
    if isinstance(keyword, str):
        keyword = punctuation_regex.sub("", keyword)
        language = detect(keyword)
        if language in ["en", "ru"]:
            words = word_tokenize(keyword, language=lang_dict.get(language))
        elif "cn" in language:
            words = jieba.lcut(keyword)
        else:
            sentence = ViTokenizer.tokenize(keyword) 
        words = [x.replace("_", " ") for x in sentence.split(" ") if "_" in x]
    elif isinstance(keyword, list):
        words = keyword.copy()
    else:
        raise TypeError("key word must be string or list of string")
    insert_result = await search_client.insert_one({
        "subject_name": subject_name,
        "keywords": words,
        "user_id": user_id,
        "time": collected_time,
        "enable": True
    })
    return str(insert_result.inserted_id)

async def get_keywords_in_selfs_newsletter():
    pipeline = [
        {
            '$match': {
                'tag': 'selfs'
            }
        }, {
            '$project': {
                'include_keywords': {
                    '$reduce': {
                        'input': '$keyword_vi.required_keyword', 
                        'initialValue': '', 
                        'in': {
                            '$concat': [
                                '$$value', '$$this', ','
                            ]
                        }
                    }
                }, 
                'exclude_keywords': '$keyword_vi.exclusion_keyword'
            }
        }, {
            '$project': {
                'phrase': {
                    '$concat': [
                        '$include_keywords', '$exclude_keywords'
                    ]
                }
            }
        }, {
            '$project': {
                'keywords': {
                    '$split': [
                        '$phrase', ','
                    ]
                }
            }
        }
    ]
    newsletter_client = get_collection_client("newsletter")
    keywords = []
    async for line in newsletter_client.aggregate(pipeline):
        keywords.extend(line.get("keywords"))
    return keywords

async def get_keywords_from_search_history(start_date, end_date, user_id:str = None):
    key_filter = {
        "$and": []
    }
    if user_id is not None:
        key_filter["$and"].append({"user_id": user_id})
        key_filter["$and"].append({"subject_name": {"$ne": ""}})
        key_filter["$and"].append({"enable": True})
    if start_date is None and end_date is None:
        key_filter.pop("$and")
    if start_date != None:
        key_filter["$and"].append({"time": {"$gte": start_date}})
    if end_date != None:
        key_filter["$and"].append({"time": {"$lte": end_date}})
    history_client = get_collection_client("search_history")
    keywords = []
    if user_id is not None:
        async for line in history_client.find(key_filter):
            keywords.append(line)
    else:
        async for line in history_client.find(key_filter):
            keywords.extend(line.get("keywords"))
    return keywords

async def disable_keyword_history(his_id:str):
    his_client = get_collection_client("search_history")
    result = await his_client.update_one({"_id": ObjectId(his_id)}, {"$set": {"enable": False}})
    return result.modified_count

# async def get_keyword_frequences(start_date, end_date, top):
#     if start_date is not None:
#         start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
#     if end_date is not None:
#         end_date = datetime.strptime(end_date, "%d/%m/%Y %H:%M:%S")
#     self_keys = await get_keywords_in_selfs_newsletter()
#     his_keys = await get_keywords_from_search_history(start_date, end_date)
#     self_keys.extend(his_keys)
#     return_data = {}
#     for key in self_keys:
#         if return_data.get(key) is None:
#             return_data[key] = 0
#         return_data[key] += 1
#     result = [ {"label": x[0], "value":x[1]} for x in sorted(return_data.items(), key=lambda item: item[1])[:top]]
#     return result


async def get_keyword_frequences(start_date, end_date, top):
    if start_date is not None:
        start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
    if end_date is not None:
        end_date = datetime.strptime(end_date, "%d/%m/%Y %H:%M:%S")
    news_col = get_collection_client("News")
    keywords = list()
    async for keys in news_col.find({'keywords': {'$exists':True}}, {"keywords": True}):
        keywords.extend(keys["keywords"])
    keydict = {}
    for key in keywords:
        if keydict.get(key) is None:
            keydict[key] = 0
        keydict[key] += 1
    result = [ {"label": x[0], "value":x[1]} for x in sorted(keydict.items(), key=lambda item: item[1], reverse=True)[:top]]
    return result

async def get_top_seven_by_self(start_date, end_date, user_id = ""):
    # defined ----------------------------
    query = {}
    query["$and"] = []

    sub_params = {
        "text_search": "",
        "sentiment": "",
        "language_source": "",
        "newsletter_id": "",
        "subject_id": None,
        "vital": "",
        "bookmarks": ""
    }

    # handle date -------------------------        
    if start_date != "" and end_date != "":
        start_date = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )

        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query["$and"].append({"pub_date": {"$gte": start_date, "$lte": end_date}})

    output_array = []
    current_date = start_date
    while current_date <= end_date:
        response = await statistics_sentiments(query, {
            "start_date": current_date,
            "end_date": current_date,
            "user_id": user_id,
            "newsletter_type": "selfs",

            **sub_params
        })
        output_array.append({"label": current_date.strftime("%d/%m/%Y"), "value": response.get("total_records")})
        current_date += timedelta(days=1)

    return output_array

async def get_top_five_by_self(start_date, end_date, user_id):
    newsletter_client = get_collection_client("newsletter")
    selfs_array = [
        {"_id": str(record.get("_id")), 
         "title": record.get("title")} for record in await newsletter_client.find({"tag": "selfs", "user_id":ObjectId(user_id)},projection={'_id': 1, "title": 1}).to_list(None)]

    # defined ----------------------------
    query = {}
    query["$and"] = []

    sub_params = {
        "text_search": "",
        "sentiment": "",
        "language_source": "",
        "subject_id": None,
        "vital": "",
        "bookmarks": "",
        "newsletter_type": None
    }

    sub_params_total = {
        "text_search": "",
        "sentiment": "",
        "language_source": "",
        "start_date": "",
        "end_date": "",
        "newsletter_id": "",
        "subject_id": None,
        "vital": "",
        "bookmarks": "",
        "newsletter_type": "selfs"
    }

    # handle date -------------------------        
    if start_date != "" and end_date != "":
        start_date = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )

        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query["$and"].append({"pub_date": {"$gte": start_date, "$lte": end_date}})


    # calculate --------------------------
    # response_total = await statistics_sentiments({}, {
    #     "user_id": user_id,
    #     **sub_params_total
    # })
    # total = response_total.get("total_records")

    output_array = []
    for record in selfs_array:
        response = await statistics_sentiments(query, {
            "start_date": start_date,
            "end_date": end_date,
            "user_id": user_id,
            "newsletter_id": record.get("_id"),

            **sub_params
        })

        output_array.append({"label": record.get("title"), "value": response.get("total_records")})

    return sorted(output_array, key=lambda x: x['value'], reverse=True)[:5]