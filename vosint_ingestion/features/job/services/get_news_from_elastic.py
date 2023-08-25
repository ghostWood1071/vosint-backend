from fastapi.responses import JSONResponse
from models import MongoRepository
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import My_ElasticSearch
from bson import ObjectId
my_es = My_ElasticSearch()

def get_news_from_newsletter_id__(list_id=None,type=None,id_nguon_nhom_nguon=None,page_number = 1, page_size = 30, start_date : str = None, end_date : str = None, sac_thai : str = None, language_source : str =None,news_letter_id: str = '',text_search = None,vital:str='',bookmarks:str='',user_id=None): 
    
    
    # list_id = None
    query = None
    try:
        start_date = start_date.split('/')[2] +'-'+ start_date.split('/')[1] +'-'+ start_date.split('/')[0]+'T00:00:00Z'
    except:
        pass
    try:
        end_date = end_date.split('/')[2] +'-'+ end_date.split('/')[1] +'-'+ end_date.split('/')[0]+'T00:00:00Z'
    except:
        pass
    if language_source:
        language_source_ = language_source.split(',')
        language_source = []
        for i in language_source_:
            language_source.append(i)

    if vital == '1':
        mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
        ls = []
        try:
            for new_id in mongo['vital_list']:
                ls.append(str(new_id))
        except:
            pass
        if ls ==[]:
            return []
        list_id = ls

    elif bookmarks == '1':
        mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
        ls = []
        kt_rong = 1
        try:
            for new_id in mongo['news_bookmarks']:
                ls.append(str(new_id))
        except:
           pass
        if ls ==[]:
            return []
        list_id = ls 
    
    if news_letter_id != '' and news_letter_id != None:
        a = MongoRepository().get_one(collection_name='newsletter',filter_spec={"_id":news_letter_id})

    if news_letter_id != '' and a['tag'] == 'gio_tin':
        ls = []
        kt_rong = 1
        try:
            for new_id in a['news_id']:
                ls.append(str(new_id))
        except:
           pass
        if ls ==[]:
            return []
        list_id = ls 

    if news_letter_id != '' and a['tag'] != 'gio_tin':
        if a['is_sample']:
            query = ''
            first_flat = 1
            try:
                for i in a['required_keyword_extract']:
                    if first_flat == 1:
                        first_flat = 0 
                        query += '('
                    else:
                        query += '| ('
                    j = i.split(',')
                    
                    for k in j:
                        query += '+'+'\"' + k + '\"'
                    query += ')'
            except:
                pass
        else:

            first_lang = 1
            query = ''
            ### vi
            query_vi = ''
            first_flat = 1
            try:
                for i in a['keyword_vi']['required_keyword']:
                    if first_flat == 1:
                        first_flat = 0 
                        query_vi += '('
                    else:
                        query_vi += '| ('
                    j = i.split(',')
                    
                    for k in j:
                        query_vi += '+'+'\"' + k + '\"'
                    query_vi += ')'
            except:
                pass
            try:
                j = a['keyword_vi']['exclusion_keyword'].split(',')
                for k in j:
                    query_vi += '-'+'\"' + k + '\"'
            except:
                pass

            ### cn
            query_cn = ''
            first_flat = 1
            try:
                for i in a['keyword_vn']['required_keyword']:
                    if first_flat == 1:
                        first_flat = 0 
                        query_cn += '('
                    else:
                        query_cn += '| ('
                    j = i.split(',')
                    
                    for k in j:
                        query_cn += '+'+'\"' + k + '\"'
                    query_cn += ')'
            except:
                pass
            try:
                j = a['keyword_cn']['exclusion_keyword'].split(',')
                for k in j:
                    query_cn += '-'+'\"' + k + '\"'
            except:
                pass

            ### cn
            query_ru = ''
            first_flat = 1
            try:
                for i in a['keyword_ru']['required_keyword']:
                    if first_flat == 1:
                        first_flat = 0 
                        query_ru += '('
                    else:
                        query_ru += '| ('
                    j = i.split(',')
                    
                    for k in j:
                        query_ru += '+'+'\"' + k + '\"'
                    query_ru += ')'
            except:
                pass
            try:
                j = a['keyword_ru']['exclusion_keyword'].split(',')
                for k in j:
                    query_ru += '-'+'\"' + k + '\"'
            except:
                pass

            ### cn
            query_en = ''
            first_flat = 1
            try:
                for i in a['keyword_en']['required_keyword']:
                    if first_flat == 1:
                        first_flat = 0 
                        query_en += '('
                    else:
                        query_en += '| ('
                    j = i.split(',')
                    
                    for k in j:
                        query_en += '+'+'\"' + k + '\"'
                    query_en += ')'
            except:
                pass
            try:
                j = a['keyword_en']['exclusion_keyword'].split(',')
                for k in j:
                    query_en += '-'+'\"' + k + '\"'
            except:
                pass
            
            if query_vi != '':
                if first_lang == 1:
                    first_lang = 0
                    query += '('+query_vi+')'
            if query_en != '':
                if first_lang == 1:
                    first_lang = 0
                    query += '('+query_en+')'
                else:
                    query += '| ('+query_en+')'
            if query_ru != '':
                if first_lang == 1:
                    first_lang = 0
                    query += '('+query_ru+')'
                else:
                    query += '| ('+query_ru+')'
            if query_cn != '':
                if first_lang == 1:
                    first_lang = 0
                    query += '('+query_cn+')'
                else:
                    query += '| ('+query_cn+')'
    list_source_name = None
    if type == 'source':
            name = MongoRepository().get_one(collection_name="infor",filter_spec={"_id":id_nguon_nhom_nguon})['name']
            list_source_name =[]
            list_source_name.append('"'+name+'"')
    elif type == 'source_group':
            name = MongoRepository().get_one(collection_name="Source",filter_spec={"_id":id_nguon_nhom_nguon})['news']
            list_source_name =[]
            for i in name:
                list_source_name.append('"'+i["name"]+'"')
    
    if text_search == None and list_source_name == None:
        pipeline_dtos = my_es.search_main(index_name='vosint',query=query,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai,list_id=list_id,size=(int(page_number))*int(page_size))
    elif text_search == None and list_source_name != None:
         pipeline_dtos = my_es.search_main(index_name='vosint',query=query,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai,list_id=list_id,list_source_name=list_source_name,size=(int(page_number))*int(page_size))
    else:
        if list_source_name == None:
            pipeline_dtos = my_es.search_main(index_name='vosint',query=query,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai,list_id=list_id,size=(int(page_number))*int(page_size))
        else:
            pipeline_dtos = my_es.search_main(index_name='vosint',query=query,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai,list_id=list_id,list_source_name=list_source_name,size=(int(page_number))*int(page_size))
        if list_id==None:
            list_id = []
        for i in range(len(pipeline_dtos)):
            list_id.append(pipeline_dtos[i]['_source']['id'])
        if text_search and list_id!= []:
            pipeline_dtos = my_es.search_main(index_name='vosint',query=text_search,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai,list_id=list_id)
    list_id = []
    query = {}
    # query['$and']=[]
    if pipeline_dtos == []:
        return JSONResponse({"success": True,"total_record":0, "result": None})
    for i in range(len(pipeline_dtos)):
        try:
            #pipeline_dtos[i]['_source']['_id'] = pipeline_dtos[i]['_source']['id']
            #print('aaaaaaaaaaaaa',pipeline_dtos[i]['_source']['id'])
            # list_id.append(pipeline_dtos[i]['_source']['id'])
            
            
            list_id.append({'_id':ObjectId(str(pipeline_dtos[i]['_source']['id']))})

            if len(list_id) != 0:
                query['$or'] = list_id
        except:
            pass
        # pipeline_dtos[i] = pipeline_dtos[i]['_source'].copy()
    # if str(query) == "{'$and': []}":
    #     query = {}
    a,_ = MongoRepository().get_many_News(collection_name='News',filter_spec=query)
    for document in pipeline_dtos:
        for key in document:
            document[key] = str(document[key])
    for i in a:
        try:
            i["_id"] = str(i["_id"])
        except:
            pass
        try:
            i['pub_date']= str(i['pub_date'])
        except:
            pass
    return JSONResponse({"success": True,"total_record":len(pipeline_dtos)+1, "result": a[(int(page_number)-1)*int(page_size):(int(page_number))*int(page_size)]})
