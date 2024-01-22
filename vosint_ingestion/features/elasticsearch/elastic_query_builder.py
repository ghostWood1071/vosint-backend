from models import MongoRepository
from bson import ObjectId

categories = {
    "vital": "vital_list",
    "bookmark":  "news_bookmarks", 

}

language_dict = {k:f'keyword_{k}' for k in ['vi', 'en', 'ru', 'cn'] }

#---------------- get related things ---------------------
def get_news_category(_ids):
    data, _ = MongoRepository().get_many(
        collection_name="News",
        order_spec=["pub_date", "created_at"],
        filter_spec={"_id": {"$in": _ids}},
    )

    result = []
    for item in data:
        item["_id"] = str(item.get("_id"))
        item["pub_date"] = str(item.get("pub_date"))

        result.append(item)

    result = get_optimized(result)

    return result

def get_optimized(result):
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

    for record in result:
        try:
            record["data:content"] = record["data:content"][0:limit_string]
            record["data:content_translate"] = record["data:content_translate"][
                0:limit_string
            ]
        except:
            pass
        for key in list_fields:
            record.pop(key, None)
    return result

def get_news_by_category(user_id:str, text_search:str, category:str)->list[str]:
    mongo = MongoRepository().get_one(
            collection_name="users", filter_spec={"_id": user_id}
        )
    ls = []
    return_data = None
    try:
        for new_id in mongo[categories.get(category)]:
            ls.append(str(new_id))
    except:
        pass
    if ls == []:
        return_data = []
    list_id = ls
    if text_search == "" or text_search == None:
        _ids = [ObjectId(item) for item in list_id]
        return_data = get_news_category(_ids)
    return {
        "list_id": list_id, 
        "data": return_data
    }

def get_news_from_cart(news_letter:any, text_search:str):
    # cart is a type of newsletter
    # newsletter has 3 types: gio_tin, linh_vuc, chu_de
    ls = []
    return_data = None
    try:
        for new_id in news_letter["news_id"]:
            ls.append(str(new_id))
    except:
        pass
    if ls == []:
        return_data = []
    list_id = ls

    if text_search == "" or text_search == None:
        _ids = [ObjectId(item) for item in list_id]
        return_data = get_news_category(_ids)
    return {
        "list_id": list_id,
        "return_data": return_data
    }

def get_source_names(type, id_source):
    #id_source la id_nguon_nhom_nguon
    list_source_name = None
    if type == "source":
        name = MongoRepository().get_one(
            collection_name="info", filter_spec={"_id": id_source}
        )["name"]
        list_source_name = []
        list_source_name.append('"' + name + '"')
    elif type == "source_group":
        source_group = MongoRepository().get_one(
            collection_name="Source", filter_spec={"_id": id_source}
        )
        name = source_group.get("news")
        list_source_name = []
        for i in name:
            list_source_name.append('"' + i["name"] + '"')
    return list_source_name


#--------------- build query ---------------------
def get_date(start_date, end_date):
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
    return start_date, end_date

def build_keyword(keyword_source, first_flat, exclude_source = None):
    query = ""
    try:
        for key_line in keyword_source:
            if first_flat == 1:
                first_flat = 0
                query += "("
            else:
                query += " | ("
            include_keys = key_line.split(",")
            for key in include_keys:
                #query += "+" + '"' + key + '"'
                key = key.strip(" ")
                query += f'"{key}" + '
            query = query.strip("+ ")
            query += ")"
    except:
        pass
    if exclude_source is not None:
        try:
            # exclude_keys = news_letter[lang_key]["exclusion_keyword"].split(",")
            exclude_keys = exclude_source.split(",")
            for key in exclude_keys:
                query_vi += " - " + '"' + key + '"'
        except:
            pass
    return query, first_flat

def build_keyword_by_lang(newsletter, lang, first_flat):
    lang_key = language_dict.get(lang)
    key_source = newsletter[lang_key]["required_keyword"]
    exclude_keys = newsletter[lang_key]["exclusion_keyword"]
    return build_keyword(key_source, first_flat, exclude_keys)

def combine_keyword(*keywords):
    first_lang = 1
    query = ""
    for keyword in keywords:
        if keyword != "":
            if first_lang == 1:
                first_lang = 0
                query += "(" + keyword + ")"
            else:
                query += "| (" + keyword + ")"
    return query

def validate_read(pipeline_dtos, is_get_read_state):
    for i in range(len(pipeline_dtos)):
        try:
            pipeline_dtos[i]["_source"]["_id"] = pipeline_dtos[i]["_source"]["id"]
        except:
            pass
        pipeline_dtos[i] = pipeline_dtos[i]["_source"].copy()
    if is_get_read_state:
        news_ids = [ObjectId(row["id"]) for row in pipeline_dtos]
        raw_isreads, _ = MongoRepository().get_many("News", {"_id": {"$in": news_ids}})
        isread = {}
        for raw_isread in raw_isreads:
            isread[str(raw_isread["_id"])] = raw_isread.get("list_user_read")
        for row in pipeline_dtos:
            row["list_user_read"] = isread.get(row["_id"])

def build_search_query_by_keyword(news_letter):
    query = ""
    if news_letter["is_sample"]:
            first_flat = 1
            query, first_flat = build_keyword(news_letter["required_keyword_extract"], first_flat)
       
    else:  #lay tin theo tu khoa cua nguoi dung tu dinh ngia
        query = ""
        ### vi
        first_flat = 1
        query_vi, first_flat = build_keyword_by_lang(news_letter, "vi", first_flat)
        ### cn
        query_cn, first_flat = build_keyword_by_lang(news_letter, "cn", first_flat)
        ### ru
        query_ru, first_flat = build_keyword_by_lang(news_letter, "ru", first_flat)
        ### cn
        query_en, first_flat = build_keyword_by_lang(news_letter, "en", first_flat)
        ## combine all keyword
        query = combine_keyword(query_vi, query_cn, query_ru, query_en)
    return query