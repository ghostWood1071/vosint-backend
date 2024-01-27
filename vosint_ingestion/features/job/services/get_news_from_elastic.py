from models import MongoRepository
from vosint_ingestion.features.elasticsearch.elastic_main import MyElasticSearch
from vosint_ingestion.features.elasticsearch.elastic_query_builder import *
from bson import ObjectId
from typing import *
from app.newsletter.models import NewsletterTag
from core.config import settings

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
    cat_type = None
):
    
    query = None
    index_name = settings.ELASTIC_NEWS_INDEX
    user = MongoRepository().get_one(collection_name="users", filter_spec={"_id": ObjectId(user_id)})
    ignore_sources = [] if user.get("sources") is None else user.get("sources")
    subject_ids = [] if user.get("subject_ids") is None else user.get("subject_ids")
    # date-------------------------------------------
    start_date, end_date = get_date(start_date, end_date)
    # language--------------------------------------------------------
    if language_source:
        language_source_ = language_source.split(",")
        language_source = []
        for i in language_source_:
            language_source.append(i)
    language_source = build_language(user.get("languages"), language_source)
    if language_source is None:
        return []
    
    
    # lay tin quan trong ---tin quan trọng -------------------------------------------------
    if vital == "1":
        result_search = get_news_by_category(text_search, "vital", user)
        if result_search.get("data") is not None:
            return result_search.get("data")
        list_id = result_search.get("list_id")
    # lay tin danh dau ---tin đánh dấu ---------------------------------------------------
    elif bookmarks == "1":
        result_search = get_news_by_category(text_search, "bookmark", user)
        if result_search.get("data") is not None:
            return result_search.get("data")
        list_id = result_search.get("list_id")
        

    # chu de/get newsletter --------------------------------------------------
    # get a newsletter by id and compare the tag to determind its a cart or a subject
    # input is a type: cart or subject, we just need to execute one 
    query = "*"
    query_phrase = []
    news_letter_filter = {}
    news_letters = []
    if cat_type:
        news_letter_filter["tag"] = cat_type
    else:
        news_letter_filter["_id"] = ObjectId(news_letter_id)

    
    if news_letter_id not in  ["", None] or cat_type is not None:
        news_letters, _ = MongoRepository().find(
            collection_name="newsletter", filter_spec=news_letter_filter
        )

    # nếu là giỏ tin
    if cat_type == NewsletterTag.ARCHIVE or len(news_letters) > 0:
        if len(news_letters) == 0 and cat_type == NewsletterTag.ARCHIVE:
            return []
        if len(news_letters) > 0:
            if news_letters[0].get("tag") == NewsletterTag.ARCHIVE:
                result_search = get_news_from_cart(news_letters, text_search)
                if result_search.get("return_data") is not None:
                    return result_search.get("return_data")
                list_id = result_search.get("list_id")
    #khong phai la gio tin
    for news_letter in news_letters:
        if news_letter["tag"] == NewsletterTag.SELFS:
            tmp_query = build_search_query_by_keyword(news_letter)
            if tmp_query not in [None, ""]:
                query_phrase.append(tmp_query)
    
    if len(query_phrase) > 0:
        query = " | ".join([f'({x})' for x in query_phrase])

    subject_query = " | ".join([f'"{x}"' for x in subject_ids])

    if text_search !=None and text_search != "":
            query = f'({query}) + ("{text_search}")'

    pipeline_dtos = my_es.search_main(
        index_name=index_name,
        query=query,
        gte=start_date,
        lte=end_date,
        lang=language_source,
        sentiment=sac_thai,
        list_id=list_id,
        size=(int(page_number)) * int(page_size),
        list_fields=list_fields,
        subject_id = subject_query, 
        list_source_id= ignore_sources
    )
        
    if list_id == None:
        list_id = []

    for i in range(len(pipeline_dtos)):
        list_id.append(pipeline_dtos[i]["_source"]["id"])

   
    validate_read(pipeline_dtos, is_get_read_state)
    
    return pipeline_dtos
