from models import MongoRepository
from vosint_ingestion.features.elasticsearch.elastic_main import MyElasticSearch
from vosint_ingestion.features.elasticsearch.elastic_query_builder import *
from bson import ObjectId
from typing import *


my_es = MyElasticSearch()

def get_news_from_newsletter_id__(
    list_id=None, # a list of news id that can limit the result of elastic
    type=None,
    id_nguon_nhom_nguon=None,
    page_number=1,
    page_size=100,
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
    list_fields=None,
):
    
    query = None
    index_name = "vosint"

    # date-------------------------------------------
    start_date, end_date = get_date(start_date, end_date)
    # language--------------------------------------------------------
    if language_source:
        language_source_ = language_source.split(",")
        language_source = []
        for i in language_source_:
            language_source.append(i)
    # lay tin quan trong ---tin quan trọng -------------------------------------------------
    if vital == "1":
        result_search = get_news_by_category(user_id, text_search, "vital")
        if result_search.get("data") is not None:
            return result_search.get("data")
        list_id = result_search.get("list_id")
    # lay tin danh dau ---tin đánh dấu ---------------------------------------------------
    elif bookmarks == "1":
        result_search = get_news_by_category(user_id, text_search, "bookmark")
        if result_search.get("data") is not None:
            return result_search.get("data")
        list_id = result_search.get("list_id")

    # chu de/get newsletter --------------------------------------------------
    if news_letter_id != "" and news_letter_id != None:
        news_letter = MongoRepository().get_one(
            collection_name="newsletter", filter_spec={"_id": news_letter_id}
        )
    
    # nếu là giỏ tin
    if news_letter_id != "" and news_letter["tag"] == "gio_tin":
        result_search = get_news_from_cart(news_letter, text_search)
        if result_search.get("return_data") is not None:
            return result_search.get("return_data")
        list_id = result_search.get("list_id")

    # nếu không là giỏ tin
    if news_letter_id != "" and news_letter["tag"] != "gio_tin":
        #lay tin theo tu khoa trich tu van ban mau
        query = build_search_query_by_keyword(news_letter)

    list_source_name = get_source_names(type, id_nguon_nhom_nguon)

    if text_search == None and list_source_name == None:
        pipeline_dtos = my_es.search_main(
            index_name=index_name,
            query=query,
            gte=start_date,
            lte=end_date,
            lang=language_source,
            sentiment=sac_thai,
            list_id=list_id,
            size=(int(page_number)) * int(page_size),
            list_fields=list_fields
        )
    elif text_search == None and list_source_name != None:
        pipeline_dtos = my_es.search_main(
            index_name=index_name,
            query=query,
            gte=start_date,
            lte=end_date,
            lang=language_source,
            sentiment=sac_thai,
            list_id=list_id,
            list_source_name=list_source_name,
            size=(int(page_number)) * int(page_size),
            list_fields=list_fields
        )
    else: #text_search != None and list_source_name != None
        if text_search !=None and text_search != "":
            query = f'({query}) +("{text_search}")'

        if list_source_name == None:
            pipeline_dtos = my_es.search_main(
                index_name=index_name,
                query=query,
                gte=start_date,
                lte=end_date,
                lang=language_source,
                sentiment=sac_thai,
                list_id=list_id,
                size=(int(page_number)) * int(page_size),
                list_fields=list_fields
            )
        else:
            pipeline_dtos = my_es.search_main(
                index_name=index_name,
                query=query,
                gte=start_date,
                lte=end_date,
                lang=language_source,
                sentiment=sac_thai,
                list_id=list_id,
                list_source_name=list_source_name,
                size=(int(page_number)) * int(page_size),
                list_fields=list_fields
            )
        if list_id == None:
            list_id = []

        for i in range(len(pipeline_dtos)):
            list_id.append(pipeline_dtos[i]["_source"]["id"])

   
    validate_read(pipeline_dtos, is_get_read_state)
    
    return pipeline_dtos
