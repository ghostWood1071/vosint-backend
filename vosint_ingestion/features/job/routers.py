from fastapi import APIRouter
from bson import ObjectId
import requests
from fastapi.responses import JSONResponse
import time
from .jobcontroller import JobController
from datetime import datetime
from typing import List
from models import MongoRepository
from fastapi_jwt_auth import AuthJWT
from fastapi.params import Body, Depends
from vosint_ingestion.features.elasticsearch.elastic_main import MyElasticSearch
from datetime import datetime

my_es = MyElasticSearch()
from pydantic import BaseModel
from db.init_db import get_collection_client
from vosint_ingestion.features.job.services.get_news_from_elastic import (
    get_news_from_newsletter_id__,
    build_search_query_by_keyword
)
from vosint_ingestion.features.elasticsearch.elastic_query_builder import build_language
from core.config import settings
from datetime import timedelta
import asyncio
import json
import re
from app.newsletter.models import NewsletterTag

ttxvn_client = get_collection_client("ttxvn")


class Translate(BaseModel):
    lang: str
    content: str


class elt(BaseModel):
    page_number: int = 1
    page_size: int = 30
    newsletter_id: str = ""  # sử dụng trong bảo newletter ko cần tự làm newList
    newList: List[
        str
    ] = []  # Trong trường hợp phát sinh, tìm kiếm trong 1 newslist nào đó
    groupType: str = None  # vital or bookmarks or ko truyền
    search_Query: str = None  # "abc" người dùng nhập
    startDate: str = None  # 17/08/2023
    endDate: str = None  # 17/08/2023
    langs: str = None  #'vi','en', 'ru' ví dụ vi,en hoặc en,ru hoặc vi
    sentiment: str = None  #'0' trung tinh, '1' tích cực, '2' tiêu cực, all ko truyền
    id_nguon_nhom_nguon: str = None  #'id source' or 'id source_group'
    type: str = None  #'source' or 'source_group'


job_controller = JobController()
router = APIRouter()




@router.post("/api/get_news_from_elt")
async def get_news_from_elt(elt: elt, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    list_fields = [
        "source_favicon",
        "source_name",
        "source_host_name",
        "source_language",
        "source_publishing_country",
        "data:title",
        "data:content",
        "pub_date",
        "data:title_translate",
        "data:content_translate",
        "data:class_sacthai",
        "data:url",
        "id",
        "_id",
        "list_user_read",
    ]
    vital = ""
    bookmarks = ""
    cat_type = None

    if elt.groupType == "vital":
        vital = "1"
    elif elt.groupType == "bookmarks":
        bookmarks = "1"
    elif elt.groupType in [NewsletterTag.ARCHIVE, NewsletterTag.SELFS]:
        cat_type = elt.groupType
        
    result_elt = get_news_from_newsletter_id__(
        user_id=user_id,
        list_id=elt.newList,
        type=elt.type,
        id_nguon_nhom_nguon=elt.id_nguon_nhom_nguon,
        page_number=elt.page_number,
        page_size=elt.page_size,
        start_date=elt.startDate,
        end_date=elt.endDate,
        sac_thai=elt.sentiment,
        language_source=elt.langs,
        news_letter_id=elt.newsletter_id,
        text_search=elt.search_Query,
        vital=vital,
        bookmarks=bookmarks,
        is_get_read_state=True,
        list_fields=list_fields,
        cat_type = cat_type
    )

    limit_string = 270

    for record in result_elt:
        try:
            record["data:content"] = record["data:content"][0:limit_string]
            record["data:content_translate"] = record["data:content_translate"][
                0:limit_string
            ]
        except:
            pass

    return JSONResponse(
        {
            "success": True,
            "total_record": len(result_elt),
            "result": result_elt[
                (int(elt.page_number) - 1)
                * int(elt.page_size) : (int(elt.page_number))
                * int(elt.page_size)
            ],
        }
    )


@router.post("/api/start_job/{pipeline_id}")
def start_job(pipeline_id: str):
    return JSONResponse(job_controller.start_job(pipeline_id))


@router.post("/api/start_all_jobs")
def start_all_jobs():  # Danh sách Pipeline Id phân tách nhau bởi dấu , (VD: 636b5322243dd7a386d65cbc,636b695bda1ea6210d1b397f)
    return JSONResponse(job_controller.start_all_jobs(None))


@router.post("/api/stop_job/{pipeline_id}")
def stop_job(pipeline_id: str):
    return JSONResponse(job_controller.stop_job(pipeline_id))


@router.post("/api/stop_all_jobs")
def stop_all_jobs():
    return JSONResponse(job_controller.stop_all_jobs(None))


@router.get("/api/get_news_from_id_source")
def get_news_from_id_source(
    id="",
    type="",
    page_number=1,
    page_size=5,
    start_date: str = None,
    end_date: str = None,
    sac_thai: str = None,
    language_source: str = None,
    text_search=None,
):
    try:
        start_date = (
            start_date.split("/")[2]
            + "-"
            + start_date.split("/")[1]
            + "-"
            + start_date.split("/")[0]
            + "T00:00:00Z"
        )
    except:
        pass
    try:
        end_date = (
            end_date.split("/")[2]
            + "-"
            + end_date.split("/")[1]
            + "-"
            + end_date.split("/")[0]
            + "T00:00:00Z"
        )
    except:
        pass
    if language_source:
        language_source_ = language_source.split(",")
        language_source = []
        for i in language_source_:
            language_source.append(i)
    return JSONResponse(
        job_controller.get_news_from_id_source(
            id,
            type,
            page_number,
            page_size,
            start_date,
            end_date,
            sac_thai,
            language_source,
            text_search,
        )
    )


@router.post("/api/run_only_job/{pipeline_id}")
def run_only_job(pipeline_id: str, mode_test=True):
    if str(mode_test) == "True" or str(mode_test) == "true":
        mode_test = True
    result = job_controller.run_only(pipeline_id, mode_test)
    return result


@router.post("/api/create_required_keyword}")
def create_required_keyword(newsletter_id: str):
    return JSONResponse(job_controller.create_required_keyword(newsletter_id))


def find_child(_id, list_id_find_child):
    list_id_find_child.append(str(_id))
    child_subjects, child_count = MongoRepository().get_many_d(
        collection_name="newsletter", filter_spec={"parent_id": _id}
    )
    if child_count == 0:
        return str(_id)
    tmp = []
    for child in child_subjects:
        tmp.append(find_child(ObjectId(child["_id"]), list_id_find_child))
    return {str(_id): tmp}


def process_date(start_date, end_date):
    try:
        start_date = (
            start_date.split("/")[2]
            + "-"
            + start_date.split("/")[1]
            + "-"
            + start_date.split("/")[0]
            + "T00:00:00Z"
        )
    except:
        pass
    try:
        end_date = (
            end_date.split("/")[2]
            + "-"
            + end_date.split("/")[1]
            + "-"
            + end_date.split("/")[0]
            + "T23:59:59Z"
        )
    except:
        pass

    # news_letter_list_id = news_letter_list_id.split(',')
    if start_date == None and end_date == None:
        end_date = datetime.now().strftime("%Y-%m-%d") + "T23:59:59Z"
        start_date = (datetime.now() - timedelta(days=30)).strftime(
            "%Y-%m-%d"
        ) + "T00:00:00Z"
    return start_date, end_date


def get_children_info(child_id_list):
    info_tree = []
    for news_letter_id in child_id_list:
        a = MongoRepository().get_one(
            collection_name="newsletter",
            filter_spec={"_id": news_letter_id},
            filter_other={"_id": 1, "title": 1, "parent_id": 1},
        )
        a["_id"] = str(a["_id"])
        try:
            a["parent_id"] = str(a["parent_id"])
        except:
            pass
        info_tree.append(a)
    return info_tree


def build_keyword_query(query, keywords):
    query = ""
    first_flat = 1
    try:
        for keyword in keywords:
            if first_flat == 1:
                first_flat = 0
                query += "("
            else:
                query += "| ("
            keyword_arr = keyword.split(",")

            for keyword in keyword_arr:
                query += "+" + '"' + keyword + '"'
            query += ")"
    except:
        pass
    return query


def build_language_keyword_query(query, lang, keywords):
    query = ""
    first_flat = 1
    try:
        for keyword in keywords[lang]["required_keyword"]:
            if first_flat == 1:
                first_flat = 0
                query += "("
            else:
                query += "| ("
            keyword_arr = [key.strip() for key in keyword.split(",")]

            for keyword in keyword_arr:
                if keyword != "":
                    query += "+" + '"' + keyword + '"'
            query += ")"
    except:
        pass
    try:
        exclude_arr = keywords[lang]["exclusion_keyword"].split(",")
        for key_exclude in exclude_arr:
            if key_exclude != "":
                query += "-" + '"' + key_exclude + '"'
    except:
        pass
    return query


def summarize_query_keyword(keywords, first_lang):
    query = ""
    for keyword in keywords:
        if keyword != "":
            if first_lang == 1:
                first_lang = 0
                query += "(" + keyword + ")"
    return query



@router.get("/api/get_result_job/News_search")
def News_search(
    text_search="*",
    page_number=1,
    page_size=30,
    start_date: str = None,
    end_date: str = None,
    sac_thai: str = None,
    language_source: str = None,
    news_letter_id: str = "",
    authorize: AuthJWT = Depends(),
    vital: str = "",
    bookmarks: str = "",
):
    try:
        start_date = (
            start_date.split("/")[2]
            + "-"
            + start_date.split("/")[1]
            + "-"
            + start_date.split("/")[0]
            + "T00:00:00Z"
        )
    except:
        pass
    # print(start_date)
    try:
        end_date = (
            end_date.split("/")[2]
            + "-"
            + end_date.split("/")[1]
            + "-"
            + end_date.split("/")[0]
            + "T00:00:00Z"
        )
    except:
        pass
    # print(end_date)
    pipeline_dtos = my_es.search_main(
        index_name=settings.ELASTIC_NEWS_INDEX,
        query=text_search,
        gte=start_date,
        lte=end_date,
        lang=language_source,
        sentiment=sac_thai,
    )

    return JSONResponse(
        {
            "success": True,
            "result": pipeline_dtos[
                (int(page_number) - 1)
                * int(page_size) : (int(page_number))
                * int(page_size)
            ],
        }
    )


@router.get("/api/get_result_job/News")
def get_result_job(
    order=None,
    text_search="",
    page_number=None,
    page_size=None,
    start_date: str = "",
    end_date: str = "",
    sac_thai: str = "",
    language_source: str = "",
    news_letter_id: str = "",
    authorize: AuthJWT = Depends(),
    vital: str = "",
    bookmarks: str = "",
    subject_id: str = None
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = MongoRepository().get_one(collection_name="users", filter_spec={"_id": ObjectId(user_id)})
    subject_ids = [] if user.get("subject_ids") is None else user.get("subject_ids")
    user_langs =  [] if user.get("languages") is None else user.get("languages")
    if len(user_langs) == 0:
        return {
            "success": True,
            "total_record": 0,
            "result": []
        }
    user_ignore_sources = [] if user.get("sources") is None else user.get("sources")
    try:
        query = {}
        query["$and"] = []

        # -----------date time filter -----------------
        if start_date != "" and end_date != "":
            if text_search != "":
                start_date = (
                    start_date.split("/")[2]
                    + "-"
                    + start_date.split("/")[1]
                    + "-"
                    + start_date.split("/")[0]
                    + "T00:00:00Z"
                )
                end_date = (
                    end_date.split("/")[2]
                    + "-"
                    + end_date.split("/")[1]
                    + "-"
                    + end_date.split("/")[0]
                    + "T00:00:00Z"
                )

            if text_search == None or text_search == "":
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

                query["$and"].append(
                    {"pub_date": {"$gte": start_date, "$lte": end_date}}
                )
        elif start_date != "":
            if text_search != "":
                start_date = (
                    start_date.split("/")[2]
                    + "-"
                    + start_date.split("/")[1]
                    + "-"
                    + start_date.split("/")[0]
                    + "T00:00:00Z"
                )

            if text_search == None or text_search == "":
                start_date = datetime(
                    int(start_date.split("/")[2]),
                    int(start_date.split("/")[1]),
                    int(start_date.split("/")[0]),
                )
                query["$and"].append({"pub_date": {"$gte": start_date}})
        elif end_date != "":
            if text_search != "":
                end_date = (
                    end_date.split("/")[2]
                    + "-"
                    + end_date.split("/")[1]
                    + "-"
                    + end_date.split("/")[0]
                    + "T00:00:00Z"
                )
            if text_search == None or text_search == "":
                end_date = datetime(
                    int(end_date.split("/")[2]),
                    int(end_date.split("/")[1]),
                    int(end_date.split("/")[0]),
                )
                query["$and"].append({"pub_date": {"$lte": end_date}})
        # -----------sentiment filter -----------------
        if sac_thai != "" and sac_thai != "all":
            query["$and"].append({"data:class_sacthai": sac_thai})
        # -----------languages filter -----------------
        if language_source != "":
            language_source = [x.strip() for x in language_source.split(",")]
            language_source = build_language(user.get("languages"), language_source)
            if language_source is not None:
                query["$and"].append({"source_language": {"$in": language_source.copy()}})
            else:
                return {
                    "success": True,
                    "total_record": 0,
                    "result": []
                }
        else:
            if len(user_langs) > 0:
                query["$and"].append({"source_language": {"$in": user_langs}})
                language_source = user_langs
        # -----------subject filter -------------------
        if subject_id not in ["", None]:
            query["$and"].append({"subject_id": subject_id})
        else:
            query["$and"].append({"subject_id": {"$in": subject_ids}})
        
        if len(user_ignore_sources) > 0:
            query["$and"].append({
                "source_id": {"$nin": user_ignore_sources}
            })
        if news_letter_id != "":
            mongo = MongoRepository().get_one(
                collection_name="newsletter", filter_spec={"_id": news_letter_id}
            )
            ls = []
            kt_rong = 1
            try:
                for new_id in mongo["news_id"]:
                    ls.append({"_id": new_id})
                    kt_rong = 0
                if kt_rong == 0:
                    query["$and"].append({"$or": ls.copy()})
            except:
                if kt_rong == 1:
                    query["$and"].append(
                        {"khong_lay_gi": "bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka"}
                    )
        elif vital == "1":
            ls = []
            kt_rong = 1
            try:
                for new_id in user["vital_list"]:
                    ls.append({"_id": new_id})
                    kt_rong = 0
                if kt_rong == 0:
                    query["$and"].append({"$or": ls.copy()})
            except:
                if kt_rong == 1:
                    query["$and"].append(
                        {"khong_lay_gi": "bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka"}
                    )
        elif bookmarks == "1":
            ls = []
            kt_rong = 1
            try:
                for new_id in user["news_bookmarks"]:
                    ls.append({"_id": new_id})
                    kt_rong = 0
                if kt_rong == 0:
                    query["$and"].append({"$or": ls.copy()})
            except:
                if kt_rong == 1:
                    query["$and"].append(
                        {"khong_lay_gi": "bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka"}
                    )
        elif text_search != "":
            if subject_id in ["", None]:
                subject_id = " | ".join([f'"{x}"' for x in subject_ids])
            pipeline_dtos = my_es.search_main(
                index_name=settings.ELASTIC_NEWS_INDEX,
                query=text_search,
                gte=start_date,
                lte=end_date,
                lang=language_source,
                sentiment=sac_thai,
                size=(int(page_number)) * int(page_size),
                subject_id = subject_id, 
                list_source_id=user_ignore_sources
            )

            total_record = len(pipeline_dtos)
            for i in range(len(pipeline_dtos)):
                try:
                    pipeline_dtos[i]["_source"]["_id"] = pipeline_dtos[i]["_source"]["id"]
                except:
                    pass
                pipeline_dtos[i] = pipeline_dtos[i]["_source"].copy()

            news_ids = [ObjectId(row["id"]) for row in pipeline_dtos]
            raw_isreads, _ = MongoRepository().get_many(
                "News", {"_id": {"$in": news_ids}}
            )
            isread = {}
            for raw_isread in raw_isreads:
                isread[str(raw_isread["_id"])] = raw_isread.get("list_user_read")
            for row in pipeline_dtos:
                row["list_user_read"] = isread.get(row["_id"])

            result = pipeline_dtos[
                (int(page_number) - 1)
                * int(page_size) : (int(page_number))
                * int(page_size)
            ]
    except Exception as e:
        query = {}
    if str(query) == "{'$and': []}":
        query = {}

    # order="data: gtitle"
    if text_search == None or text_search == "":
        result = job_controller.get_result_job(
            "News", order, page_number, page_size, filter=query
        )

    list_fields = [
        "data:html",
        "keywords",
        "source_publishing_country",
        "source_source_type",
        "data:class_linhvuc",
        "data:class_chude",
        "created",
        # "created_at",
        "id_social",
        "modified_at",
    ]

    limit_string = 270

    current_result = (
        result["result"] if (text_search == None or text_search == "") else result
    )
    for record in current_result:
        try:
            record["data:content"] = record["data:content"][0:limit_string]
            record["data:content_translate"] = record["data:content_translate"][
                0:limit_string
            ]
        except:
            pass
        for key in list_fields:
            record.pop(key, None)

    return (
        result
        if (text_search == None or text_search == "")
        else {"result": result, "total_record": total_record}
    )


@router.get("/api/get_table")
def get_table(
    name,
    id=None,
    order=None,
    page_number=None,
    page_size=None,
    text_search="",
    start_date="",
    end_date="",
    sac_thai="",
    # language_source="",
):
    query = {}
    query["$and"] = []

    if id != None:
        query["id"] = str(id)

    # filter by start_date, end_date, text_search
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

        end_date = end_date.replace(hour=23, minute=59, second=59)

        start_date = str(start_date).replace("-", "/")
        end_date = str(end_date).replace("-", "/")
        query["$and"].append({"created_at": {"$gte": start_date, "$lte": end_date}})

    elif start_date != "":
        start_date = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )
        start_date = str(start_date).replace("-", "/")
        query["$and"].append({"created_at": {"$gte": start_date}})

    elif end_date != "":
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_date = str(end_date).replace("-", "/")
        query["$and"].append({"created_at": {"$lte": end_date}})

    if sac_thai != "" and sac_thai != "all":
        query["$and"].append({"sentiment": sac_thai})

    if text_search != "":
        query["$and"].append(
            {
                "$or": [
                    {"header": {"$regex": text_search, "$options": "i"}},
                    {"content": {"$regex": text_search, "$options": "i"}},
                ]
            }
        )

    if str(query) == "{'$and': []}":
        query = {}

    # limit_string = 270

    # result = job_controller.get_result_job(
    #     name, order, page_number, page_size, filter=query
    # )

    # list_fields = [
    #     "id_data_ft",
    #     "footer_date",
    #     "footer_type",
    #     "video_id",
    #     "video_link",
    #     "post_link",
    #     "post_id",
    #     "user_id",
    # ]

    # for record in result["result"]:
    #     try:
    #         record["content"] = record["content"][0:limit_string]
    #     except:
    #         pass
    #     for key in list_fields:
    #         record.pop(key, None)

    # return result

    return JSONResponse(
        job_controller.get_result_job(name, order, page_number, page_size, filter=query)
    )


@router.get("/api/test/{pipeline_id}")
def get_result_job(pipeline_id):
    return JSONResponse(job_controller.test_only(pipeline_id))


@router.get("/api/get_log_history/{pipeline_id}")
def get_log_history(pipeline_id: str, order=None, page_number=None, page_size=None):
    return JSONResponse(
        job_controller.get_log_history(pipeline_id, order, page_number, page_size)
    )


@router.get("/api/get_log_history_last/{pipeline_id}")
def get_log_history(pipeline_id: str):
    try:
        return JSONResponse(
            job_controller.get_log_history_last(pipeline_id)["result"][-1]
        )
    except:
        return JSONResponse(job_controller.get_log_history_last(pipeline_id)["result"])


@router.get("/api/get_log_history_error_or_getnews/{pipeline_id}")
def get_log_history_error_or_getnews(
    pipeline_id: str,
    order=None,
    page_number=None,
    page_size=None,
    start_date: str = None,
    end_date: str = None,
):
    job_controller_v2 = JobController()
    return JSONResponse(
        job_controller_v2.get_log_history_error_or_getnews(
            pipeline_id, order, page_number, page_size, start_date, end_date
        )
    )


@router.get("/get-total-crawl")
async def get_total_crawl(current_date: str):
    # current_date = datetime.utcnow().strftime("%d/%m/%Y")

    start_date = datetime(
        int(current_date.split("/")[2]),
        int(current_date.split("/")[1]),
        int(current_date.split("/")[0]),
    )

    end_date = datetime(
        int(current_date.split("/")[2]),
        int(current_date.split("/")[1]),
        int(current_date.split("/")[0]),
    )

    end_date = end_date.replace(hour=23, minute=59, second=59)

    filter_spec = {
        "$and": [
            {"PublishDate": {"$gte": start_date}},
            {"PublishDate": {"$lte": end_date}},
            {"content": {"$exists": True}},
            {"content": {"$ne": ""}},
            {"content": {"$ne": None}},
        ]
    }
    total = 0

    total = await ttxvn_client.count_documents(filter_spec)
    return total


@router.post("/api/translate")
def translate(data: Translate):
    result = job_controller.translate(data.lang, data.content)
    return JSONResponse({"results": result})


