from .services import JobService
from vosint_ingestion.features.job.services.get_news_from_elastic import (
    get_news_from_newsletter_id__,
)
from bson.objectid import ObjectId
from models import MongoRepository
import requests
from core.config import settings
import json
from datetime import datetime


def get_depth(mylist):
    if isinstance(mylist, list):
        return 1 + max(get_depth(item) for item in mylist)
    else:
        return 0


class JobController:
    def __init__(self):
        self.__job_service = JobService()

    def start_job(self, pipeline_id: str):
        self.__job_service.start_job(pipeline_id)

        return {"success": True}

    def start_all_jobs(self, pipeline_ids=None):
        # Receives request data
        # pipeline_ids = request.args.get('pipeline_ids')

        self.__job_service.start_all_jobs(pipeline_ids)

        return {"success": True}

    def stop_job(self, pipeline_id: str):
        self.__job_service.stop_job(pipeline_id)

        return {"success": True}

    def stop_all_jobs(self, pipeline_ids):
        # Receives request data
        # pipeline_ids = request.args.get('pipeline_ids')

        self.__job_service.stop_all_jobs(pipeline_ids)
        return {"success": True}

    ### Doan
    def get_news_from_id_source(
        self,
        id,
        type,
        page_number,
        page_size,
        start_date,
        end_date,
        sac_thai,
        language_source,
        text_search,
    ):
        page_number = int(page_number)
        page_size = int(page_size)
        result = self.__job_service.get_news_from_id_source(
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
        return {
            "total_record": len(result),
            "result": result[
                (int(page_number) - 1)
                * int(page_size) : (int(page_number))
                * int(page_size)
            ],
        }

    def create_required_keyword(self, newsletter_id):
        try:
            self.__job_service.create_required_keyword(newsletter_id)
            return {"success": True}
        except:
            return {"success": True}

    def run_only(self, pipeline_id: str, mode_test):
        result = self.__job_service.run_only(pipeline_id, mode_test)
        return result

    def get_result_job(self, News, order, page_number, page_size, filter):
        # Receives request data
        # order = request.args.get('order')
        # order = request.args.get('order')
        # page_number = request.args.get('page_number')
        page_number = int(page_number) if page_number is not None else None
        # page_size = request.args.get('page_size')
        page_size = int(page_size) if page_size is not None else None

        # Create sort condition
        order_spec = order.split(",") if order else []

        # Calculate pagination information
        page_number = page_number if page_number else 1
        page_size = page_size if page_size else 20
        pagination_spec = {"skip": page_size * (page_number - 1), "limit": page_size}

        pipeline_dtos, total_records = self.__job_service.get_result_job(
            News, order_spec=order_spec, pagination_spec=pagination_spec, filter=filter
        )

        for i in pipeline_dtos:
            try:
                i["_id"] = str(i["_id"])
            except:
                pass
            try:
                i["pub_date"] = str(i.get("pub_date"))
                i["created"] = str(i.get("created"))
                i["id_social"] = str(i.get("id_social"))
            except:
                pass
        return {"success": True, "total_record": total_records, "result": pipeline_dtos}

    def run_one_foreach(self, pipeline_id: str):
        result = self.__job_service.run_one_foreach(pipeline_id)

        return {"result": str(result)}

    def test_only(self, pipeline_id: str):
        result = self.__job_service.test_only(pipeline_id)

        return result

    def get_log_history(self, pipeline_id: str, order, page_number, page_size):
        # Receives request data
        # order = request.args.get('order')
        # order = request.args.get('order')
        # page_number = request.args.get('page_number')
        page_number = int(page_number) if page_number is not None else None
        # page_size = request.args.get('page_size')
        page_size = int(page_size) if page_size is not None else None

        # Create sort condition
        order_spec = order.split(",") if order else []

        # Calculate pagination information
        page_number = page_number if page_number else 1
        page_size = page_size if page_size else 20
        pagination_spec = {"skip": page_size * (page_number - 1), "limit": page_size}

        result = self.__job_service.get_log_history(
            pipeline_id, order_spec=order_spec, pagination_spec=pagination_spec
        )

        return {"success": True, "total_record": result[1], "result": result[0]}

    def get_log_history_last(self, pipeline_id: str):
        result = self.__job_service.get_log_history_last(pipeline_id)

        return {"success": True, "total_record": result[1], "result": result[0]}

    def get_log_history_error_or_getnews(
        self, pipeline_id: str, order, page_number, page_size, start_date, end_date
    ):
        if start_date is not None and start_date != "":
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        if end_date is not None and end_date != "":
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        # Receives request data
        # order = request.args.get('order')
        # order = request.args.get('order')
        # page_number = request.args.get('page_number')
        page_number = int(page_number) if page_number is not None else None
        # page_size = request.args.get('page_size')
        page_size = int(page_size) if page_size is not None else None

        # Create sort condition
        order_spec = order.split(",") if order else []

        # Calculate pagination information
        page_number = page_number if page_number else 1
        page_size = page_size if page_size else 20
        pagination_spec = {"skip": page_size * (page_number - 1), "limit": page_size}

        result = self.__job_service.get_log_history_error_or_getnews(
            pipeline_id,
            order_spec=order_spec,
            pagination_spec=pagination_spec,
            start_date=start_date,
            end_date=end_date,
        )

        return {"success": True, "total_record": result[1], "result": result[0]}

    def elt_search(
        self,
        page_number,
        page_size,
        start_date,
        end_date,
        sac_thai,
        language_source,
        text_search,
        ids,
    ):
        pipeline_dtos = self.__job_service.elt_search(
            start_date, end_date, sac_thai, language_source, text_search, ids
        )
        for i in range(len(pipeline_dtos)):
            try:
                pipeline_dtos[i]["_source"]["_id"] = pipeline_dtos[i]["_source"]["id"]
            except:
                pass
            pipeline_dtos[i] = pipeline_dtos[i]["_source"].copy()
        return {
            "total_record": len(pipeline_dtos),
            "result": pipeline_dtos[
                (int(page_number) - 1)
                * int(page_size) : (int(page_number))
                * int(page_size)
            ],
        }

    def view_time_line(
        self,
        elt,
        user_id,
        vital,
        bookmarks,
    ):
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
        )
        ids = [x["id"] for x in result_elt]
        timelines, _ = MongoRepository().get_many("events", {"new_list": {"$in": ids}})
        for timeline in timelines:
            timeline["_id"] = str(timeline["_id"])
            timeline["date_created"] = str(timeline["date_created"])
        return timelines

    def search_news_by_object(
        self,
        page_number,
        page_size,
        start_date,
        end_date,
        sac_thai,
        language_source,
        text_search,
        object_id,
    ):
        filter_spec = {}
        if text_search != None and text_search != "":
            filter_spec.update(
                {"data:content": {"$regex": rf"\b{text_search}\b", "$options": "i"}}
            )
            filter_spec.update(
                {"data:title": {"$regex": rf"\b{text_search}\b", "$options": "i"}}
            )
        if end_date != None and end_date != "":
            _end_date = datetime.strptime(end_date, "%d/%m/%Y")
            filter_spec.update({"pub_date": {"$lte": _end_date}})
        if start_date != None and start_date != "":
            _start_date = datetime.strptime(start_date, "%d/%m/%Y")
            if filter_spec.get("pub_date") == None:
                filter_spec.update({"pub_date": {"$gte": _start_date}})
            else:
                filter_spec["pub_date"].update({"$gte": _start_date})

        if sac_thai != None and sac_thai != "":
            filter_spec.update({"data:class_sacthai": sac_thai})
        if language_source != None and language_source != "":
            filter_spec.update({"source_language": language_source})

        news_ids_pipe_line = [
            {"$match": {"_id": ObjectId(object_id)}},
            {"$addFields": {"arrayLength": {"$size": "$news_list"}}},
            {
                "$project": {
                    "arrayLength": 1,
                    "sub_set": {
                        "$slice": [
                            "$news_list",
                            {
                                "$subtract": [
                                    "$arrayLength",
                                    int(page_size) * int(page_number),
                                ]
                            },
                            int(page_size),
                        ]
                    },
                }
            },
        ]
        try:
            objects = MongoRepository().aggregate("object", news_ids_pipe_line)
            if len(objects) == 0:
                return {"result": [], "total_record": 0}
            news_ids = [ObjectId(news_id) for news_id in objects[0].get("sub_set")]
            total = int(objects[0].get("arrayLength"))
            filter_spec["_id"] = {"$in": news_ids}
            news, _ = MongoRepository().get_many_News("News", filter_spec, ["pub_date"])

            for row_new in news:
                row_new["_id"] = str(row_new["_id"])
                row_new["pub_date"] = str(row_new["pub_date"])
        except Exception as e:
            print(e)
            news = []
            total = 0
        return {"result": news, "total_record": total}

    def translate(self, lang, content):
        lang_dict = {"en": "english", "ru": "russian", "cn": "chinese"}
        lang_code = lang_dict.get(lang)
        req = requests.post(
            settings.TRANSLATE_API,
            data=json.dumps({"language": lang_code, "text": content}),
        )
        if req.ok:
            return req.json().get("translate_text")
        else:
            return ""

    def get_history_statistic_by_id(self, pipeline_id, start_date, end_date, n_days):
        if start_date is not None and start_date != "":
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        if end_date is not None and end_date != "":
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        return self.__job_service.get_history_statistic_by_id(
            pipeline_id, start_date, end_date, n_days
        )
