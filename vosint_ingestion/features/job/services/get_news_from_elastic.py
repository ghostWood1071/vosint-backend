from fastapi.responses import JSONResponse
from models import MongoRepository
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import (
    My_ElasticSearch,
)
from db.init_db import get_collection_client
from bson import ObjectId

my_es = My_ElasticSearch()


def get_news_from_newsletter_id__(
    list_id=None,
    type=None,
    id_nguon_nhom_nguon=None,
    page_number=1,
    page_size=30,
    start_date: str = None,
    end_date: str = None,
    sac_thai: str = None,
    language_source: str = None,
    news_letter_id: str = "",
    text_search=None,
    vital: str = "",
    bookmarks: str = "",
    user_id=None,
    is_get_read_state=False,
):
    # list_id = None
    query = None
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

    if vital == "1":
        mongo = MongoRepository().get_one(
            collection_name="users", filter_spec={"_id": user_id}
        )
        ls = []
        try:
            for new_id in mongo["vital_list"]:
                ls.append(str(new_id))
        except:
            pass
        if ls == []:
            return []
        list_id = ls

    elif bookmarks == "1":
        mongo = MongoRepository().get_one(
            collection_name="users", filter_spec={"_id": user_id}
        )
        ls = []
        kt_rong = 1
        try:
            for new_id in mongo["news_bookmarks"]:
                ls.append(str(new_id))
        except:
            pass
        if ls == []:
            return []
        list_id = ls

    if news_letter_id != "" and news_letter_id != None:
        a = MongoRepository().get_one(
            collection_name="newsletter", filter_spec={"_id": news_letter_id}
        )

    if news_letter_id != "" and a["tag"] == "gio_tin":
        ls = []
        kt_rong = 1
        try:
            for new_id in a["news_id"]:
                ls.append(str(new_id))
        except:
            pass
        if ls == []:
            return []
        list_id = ls

    if news_letter_id != "" and a["tag"] != "gio_tin":
        if a["is_sample"]:
            query = ""
            first_flat = 1
            try:
                for i in a["required_keyword_extract"]:
                    if first_flat == 1:
                        first_flat = 0
                        query += "("
                    else:
                        query += "| ("
                    j = i.split(",")

                    for k in j:
                        query += "+" + '"' + k + '"'
                    query += ")"
            except:
                pass
        else:
            first_lang = 1
            query = ""
            ### vi
            query_vi = ""
            first_flat = 1
            try:
                for i in a["keyword_vi"]["required_keyword"]:
                    if first_flat == 1:
                        first_flat = 0
                        query_vi += "("
                    else:
                        query_vi += "| ("
                    j = i.split(",")

                    for k in j:
                        query_vi += "+" + '"' + k + '"'
                    query_vi += ")"
            except:
                pass
            try:
                j = a["keyword_vi"]["exclusion_keyword"].split(",")
                for k in j:
                    query_vi += "-" + '"' + k + '"'
            except:
                pass

            ### cn
            query_cn = ""
            first_flat = 1
            try:
                for i in a["keyword_vn"]["required_keyword"]:
                    if first_flat == 1:
                        first_flat = 0
                        query_cn += "("
                    else:
                        query_cn += "| ("
                    j = i.split(",")

                    for k in j:
                        query_cn += "+" + '"' + k + '"'
                    query_cn += ")"
            except:
                pass
            try:
                j = a["keyword_cn"]["exclusion_keyword"].split(",")
                for k in j:
                    query_cn += "-" + '"' + k + '"'
            except:
                pass

            ### cn
            query_ru = ""
            first_flat = 1
            try:
                for i in a["keyword_ru"]["required_keyword"]:
                    if first_flat == 1:
                        first_flat = 0
                        query_ru += "("
                    else:
                        query_ru += "| ("
                    j = i.split(",")

                    for k in j:
                        query_ru += "+" + '"' + k + '"'
                    query_ru += ")"
            except:
                pass
            try:
                j = a["keyword_ru"]["exclusion_keyword"].split(",")
                for k in j:
                    query_ru += "-" + '"' + k + '"'
            except:
                pass

            ### cn
            query_en = ""
            first_flat = 1
            try:
                for i in a["keyword_en"]["required_keyword"]:
                    if first_flat == 1:
                        first_flat = 0
                        query_en += "("
                    else:
                        query_en += "| ("
                    j = i.split(",")

                    for k in j:
                        query_en += "+" + '"' + k + '"'
                    query_en += ")"
            except:
                pass
            try:
                j = a["keyword_en"]["exclusion_keyword"].split(",")
                for k in j:
                    query_en += "-" + '"' + k + '"'
            except:
                pass

            if query_vi != "":
                if first_lang == 1:
                    first_lang = 0
                    query += "(" + query_vi + ")"
            if query_en != "":
                if first_lang == 1:
                    first_lang = 0
                    query += "(" + query_en + ")"
                else:
                    query += "| (" + query_en + ")"
            if query_ru != "":
                if first_lang == 1:
                    first_lang = 0
                    query += "(" + query_ru + ")"
                else:
                    query += "| (" + query_ru + ")"
            if query_cn != "":
                if first_lang == 1:
                    first_lang = 0
                    query += "(" + query_cn + ")"
                else:
                    query += "| (" + query_cn + ")"
    list_source_name = None
    if type == "source":
        name = MongoRepository().get_one(
            collection_name="infor", filter_spec={"_id": id_nguon_nhom_nguon}
        )["name"]
        list_source_name = []
        list_source_name.append('"' + name + '"')
    elif type == "source_group":
        name = MongoRepository().get_one(
            collection_name="Source", filter_spec={"_id": id_nguon_nhom_nguon}
        )["news"]
        list_source_name = []
        for i in name:
            list_source_name.append('"' + i["name"] + '"')

    if text_search == None and list_source_name == None:
        pipeline_dtos = my_es.search_main(
            index_name="vosint",
            query=query,
            gte=start_date,
            lte=end_date,
            lang=language_source,
            sentiment=sac_thai,
            list_id=list_id,
        )
    elif text_search == None and list_source_name != None:
        pipeline_dtos = my_es.search_main(
            index_name="vosint",
            query=query,
            gte=start_date,
            lte=end_date,
            lang=language_source,
            sentiment=sac_thai,
            list_id=list_id,
            list_source_name=list_source_name,
        )
    else:
        if list_source_name == None:
            pipeline_dtos = my_es.search_main(
                index_name="vosint",
                query=query,
                gte=start_date,
                lte=end_date,
                lang=language_source,
                sentiment=sac_thai,
                list_id=list_id,
            )
        else:
            pipeline_dtos = my_es.search_main(
                index_name="vosint",
                query=query,
                gte=start_date,
                lte=end_date,
                lang=language_source,
                sentiment=sac_thai,
                list_id=list_id,
                list_source_name=list_source_name,
            )
        if list_id == None:
            list_id = []
        for i in range(len(pipeline_dtos)):
            list_id.append(pipeline_dtos[i]["_source"]["id"])
        pipeline_dtos = my_es.search_main(
            index_name="vosint",
            query=text_search,
            gte=start_date,
            lte=end_date,
            lang=language_source,
            sentiment=sac_thai,
            list_id=list_id,
        )

    for i in range(len(pipeline_dtos)):
        try:
            pipeline_dtos[i]["_source"]["_id"] = pipeline_dtos[i]["_source"]["id"]
        except:
            pass
        pipeline_dtos[i] = pipeline_dtos[i]["_source"].copy()
    if is_get_read_state:
        news_ids = [ObjectId(row["id"]) for row in pipeline_dtos]
        raw_isreads, _ = MongoRepository().get_many("News", {"_id": {"$in": news_ids}})
        isreads = {}
        for raw_read in raw_isreads:
            if (
                raw_read.get("is_read") != None
                and raw_read.get("list_user_read") != None
            ):
                if user_id in raw_read.get("list_user_read"):
                    # isreads.append(str(raw_read.get("_id")))
                    isreads[str(raw_read["_id"])] = True
        for row in pipeline_dtos:
            row["is_read"] = True if isreads.get(row["id"]) != None else False
    return pipeline_dtos
