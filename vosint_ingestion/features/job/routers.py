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
from vosint_ingestion.features.minh.Elasticsearch_main.elastic_main import My_ElasticSearch
my_es = My_ElasticSearch(host=['http://192.168.1.99:9200'], user='USER', password='PASS', verify_certs=False)

job_controller = JobController()
router = APIRouter()


@router.post("/api/start_job/{pipeline_id}")
def start_job(pipeline_id: str):
    return JSONResponse(job_controller.start_job(pipeline_id))


@router.post("/api/start_all_jobs")
def start_all_jobs(
    pipeline_ids,
):  # Danh sách Pipeline Id phân tách nhau bởi dấu , (VD: 636b5322243dd7a386d65cbc,636b695bda1ea6210d1b397f)
    return JSONResponse(job_controller.start_all_jobs(pipeline_ids))


@router.post("/api/stop_job/{pipeline_id}")
def stop_job(pipeline_id: str):
    return JSONResponse(job_controller.stop_job(pipeline_id))


@router.post("/api/stop_all_jobs")
def stop_all_jobs(pipeline_ids):
    return JSONResponse(job_controller.stop_all_jobs(pipeline_ids))

@router.get("/api/get_news_from_id_source")
def get_news_from_id_source(id='',type='',page_number = 1,page_size = 5,start_date : str = None, end_date : str = None, sac_thai : str = None, language_source : str =None,text_search = None):
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
    return JSONResponse(job_controller.get_news_from_id_source(id,type,page_number,page_size,start_date,end_date,sac_thai,language_source,text_search))



@router.post("/api/run_only_job/{pipeline_id}")
def run_only_job(pipeline_id: str, mode_test = True):
    if str(mode_test) == 'True' or str(mode_test) == 'true':
        mode_test = True
    # url = "http://vosint.aiacademy.edu.vn/api/pipeline/Pipeline/api/get_action_infos"
    # requests.get(url)
    # url = "http://vosint.aiacademy.edu.vn/api/pipeline/Pipeline/api/get_pipeline_by_id/"+str(pipeline_id)
    # requests.get(url)
    #time.sleep(5)
    return JSONResponse(job_controller.run_only(pipeline_id, mode_test))


# @router.post("/api/create_required_keyword}")
# def create_required_keyword(newsletter_id: str):
    
#     return JSONResponse(job_controller.create_required_keyword(newsletter_id))

# @router.get("/api/run_only_job/{pipeline_id}")
# def run_only_job(pipeline_id: str, mode_test = True):
#     return JSONResponse(job_controller.run_only(pipeline_id,mode_test))



# @router.get("/api/get_result_job/{News}")
# def get_result_job(News='News', order = None, page_number = None, page_size = None, start_date : str, end_date = str, sac_thai : str, language_source : list):
#     return JSONResponse(
#         job_controller.get_result_job(News, order, page_number, page_size, start_date, end_date, sac_thai, language_source)
#     )
# from typing import Annotated
# @router.get("/api/test__")
# def test__(q: Annotated[list[str]):
#     return JSONResponse({"a":1})

def find_child(_id,list_id_find_child):
    list_id_find_child.append(str(_id))
    
    a,_ = MongoRepository().get_many_d(collection_name="newsletter",filter_spec={"parent_id":_id})
    tmp = []
    if _ == 0:
        return str(_id)
    else:
        tmp = []
        for i in a:  
            tmp.append(find_child(_id=ObjectId(i['_id']),list_id_find_child = list_id_find_child))   
    return {str(_id):tmp}
@router.get("/api/get_event_from_newsletter_list_id")
def get_event_from_newsletter_list_id(page_number = 1, page_size = 30, start_date : str = None, end_date : str = None, sac_thai : str = None, language_source : str =None,news_letter_id: str = '', authorize: AuthJWT = Depends(),event_number = None): 
    try:
        start_date = start_date.split('/')[2] +'-'+ start_date.split('/')[1] +'-'+ start_date.split('/')[0]+'T00:00:00Z'
    except:
        pass
    try:
        end_date = end_date.split('/')[2] +'-'+ end_date.split('/')[1] +'-'+ end_date.split('/')[0]+'T00:00:00Z'
    except:
        pass
    result = []

    # news_letter_list_id = news_letter_list_id.split(',')

    #xử lý newletter parent
    list_id_find_child =[]
    tree = find_child(_id = ObjectId(news_letter_id),list_id_find_child =list_id_find_child)
    infor_tree = []
    for news_letter_id in list_id_find_child:
        a = MongoRepository().get_one(collection_name='newsletter',filter_spec={"_id":news_letter_id},filter_other={"_id":1,"title":1,"parent_id":1})
        a['_id']=str(a['_id'])
        try:
            a['parent_id']=str(a['parent_id'])
        except:
            pass
        infor_tree.append(a)
       
        try:
            a = MongoRepository().get_one(collection_name='newsletter',filter_spec={"_id":news_letter_id})
            # a['_id']=str(a['_id'])
            # try:
            #     a['parent_id']=str(a['parent_id'])
            # except:
            #     pass
            # infor_tree.append(a)
            query = ''
            first_flat = 1 
            try:
                for i in a['required_keyword']:
                    if first_flat == 1:
                        first_flat = 0 
                        query += '('
                    else:
                        query += 'or ('
                    j = i.split(',')
                    
                    for k in j:
                        query += '+'+'\"' + k + '\"'
                    query += ')'
            except:
                pass
            try:
                j = a['exclusion_keyword'].split(',')
                for k in j:
                    query += '-'+'\"' + k + '\"'
            except:
                pass
        
            pipeline_dtos = my_es.search_main(index_name='vosint',query=query,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai)
            list_link = []
            for i in pipeline_dtos:
                list_link.append({"data:url":i['_source']['data:url']})
            
            a,_ = MongoRepository().get_many_d(collection_name='News',filter_spec={'$or': list_link.copy()}, filter_other={"_id":1})
            list_id = []
            for i in a:
                list_id.append(str(i['_id']))
            
            a,_ = MongoRepository().get_many_d(collection_name='event')

        
            sk = []
            for i in a:
                try:
                    i['date_created'] = str(i['date_created'])
                except:
                    pass
                kt = 0
                # print(i['new_list'])
                # print(list_id)
                try:
                    for j in i['new_list']:
                        #print(j)
                        if kt == 1:
                            continue
                        if j in list_id:
                            i['_id']=str(i['_id']) 
                            #result.append({news_letter_id:i})
                            new_list = []
                            for _ in i['new_list']:
                                a_ = MongoRepository().get_one(collection_name='News',filter_spec={"_id":_},filter_other={"data:title":1,"data:url":1})
                                try:
                                    a_['_id'] = str(a_['_id'])
                                    # a_['pub_date'] = str(a_['pub_date'])
                                except:
                                    pass
                                new_list.append(a_)
                            i['new_list'] = new_list
                            sk.append(i)
                            kt = 1 
                        if kt == 1:
                            continue
                    #if kt == 1:
                    #    continue
                    
                except:
                    pass
            if event_number != None:
                result.append({news_letter_id:sk[:int(event_number)]})
            else:
                result.append({news_letter_id:sk})
        except:
            pass
    #return result[(int(page_number)-1)*int(page_size):(int(page_number))*int(page_size)]
    return JSONResponse({"success": True, "tree":tree,"infor_tree":infor_tree, "result": result[(int(page_number)-1)*int(page_size):(int(page_number))*int(page_size)]})


@router.get("/api/get_news_from_newsletter_id")
def get_event_from_newsletter_id(page_number = 1, page_size = 30, start_date : str = None, end_date : str = None, sac_thai : str = None, language_source : str =None,news_letter_id: str = '', authorize: AuthJWT = Depends(),text_search = None,vital:str='',bookmarks:str=''): 
    list_id = None
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
        authorize.jwt_required()
        user_id = authorize.get_jwt_subject()
        mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
        ls = []
        try:
            for new_id in mongo['vital_list']:
                ls.append({'_id':new_id})
        except:
            pass
        if ls ==[]:
            return []
        list_id = ls

    elif bookmarks == '1':
        authorize.jwt_required()
        user_id = authorize.get_jwt_subject()
        mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
        ls = []
        kt_rong = 1
        try:
            for new_id in mongo['news_bookmarks']:
                ls.append({'_id':new_id})
        except:
           pass
        if ls ==[]:
            return []
        list_id = ls  

    a = MongoRepository().get_one(collection_name='newsletter',filter_spec={"_id":news_letter_id})
    #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaâ',a)
    # query = ''
    # first_flat = 1 
    # try:
    #     for i in a['required_keyword']:
    #         if first_flat == 1:
    #             first_flat = 0 
    #             query += '('
    #         else:
    #             query += '| ('
    #         j = i.split(',')
            
    #         for k in j:
    #             query += '+'+'\"' + k + '\"'
    #         query += ')'
    # except:
    #     pass
    # try:
    #     j = a['exclusion_keyword'].split(',')
    #     for k in j:
    #         query += '-'+'\"' + k + '\"'
    # except:
    #     pass
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
        





    if text_search != None:
        query += '+(' + text_search + ')'
 
    pipeline_dtos = my_es.search_main(index_name='vosint',query=query,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai,list_id=list_id)
    # list_link = []
    # for i in pipeline_dtos:
    #     list_link.append({"data:url":i['_source']['url']})
    
    # a,_ = MongoRepository().get_many_d(collection_name='News',filter_spec={'$or': list_link.copy()}, filter_other={"_id":1})
    # list_id = []
    # for i in a:
    #     list_id.append(str(i['_id']))
    
    # a,_ = MongoRepository().get_many_d(collection_name='event')
 
    # result = []
    # for i in a:
    #     kt = 0
    #     try:
    #         for j in i['new_list']:
    #             print(j)
    #             if j in list_id:
    #                 i['_id']=str(i['_id']) 
    #                 result.append(i)
    #                 kt = 1 
    #             if kt == 1:
    #                 continue
    #         if kt == 1:
    #             continue
    #     except:
    #         pass
    for i in range(len(pipeline_dtos)):
        try:
            pipeline_dtos[i]['_source']['_id'] = pipeline_dtos[i]['_source']['id']
        except:
            pass
        pipeline_dtos[i] = pipeline_dtos[i]['_source'].copy()

    return JSONResponse({"success": True, "result": pipeline_dtos[(int(page_number)-1)*int(page_size):(int(page_number))*int(page_size)]})

@router.get("/api/get_result_job/News_search")
def News_search(text_search = '*', page_number = 1, page_size = 30, start_date : str = None, end_date : str = None, sac_thai : str = None, language_source : str =None,news_letter_id: str = '', authorize: AuthJWT = Depends(),vital:str='',bookmarks:str=''): 
    try:
        start_date = start_date.split('/')[2] +'-'+ start_date.split('/')[1] +'-'+ start_date.split('/')[0]+'T00:00:00Z'
    except:
        pass
    #print(start_date)
    try:
        end_date = end_date.split('/')[2] +'-'+ end_date.split('/')[1] +'-'+ end_date.split('/')[0]+'T00:00:00Z'
    except:
        pass
    #print(end_date)
    pipeline_dtos = my_es.search_main(index_name='vosint',query=text_search,gte=start_date,lte=end_date,lang=language_source,sentiment=sac_thai)

    # if news_letter_id != '':
    #     mongo = MongoRepository().get_one(collection_name='newsletter',filter_spec={'_id':news_letter_id})
    #     ls = []
    #     kt_rong = 1
    #     try:
    #         for new_id in mongo['news_id']:
    #             ls.append({'_id':new_id})
    #             kt_rong = 0
    #         if kt_rong == 0:
    #             for i in range(len(pipeline_dtos)):
    #                 if 
                
    #     except:
    #         pass
    # elif vital == '1':
    #     mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
    #     ls = []
    #     kt_rong = 1
    #     try:
    #         for new_id in mongo['vital_list']:
    #             ls.append({'_id':new_id})
    #             kt_rong = 0
    #         if kt_rong == 0:
                
    #     except:
    #         pass

    # elif bookmarks == '1':
    #     mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
    #     ls = []
    #     kt_rong = 1
    #     try:
    #         for new_id in mongo['news_bookmarks']:
    #             ls.append({'_id':new_id})
    #             kt_rong = 0
    #         if kt_rong == 0:
                
    #     except:
    #        pass

    return JSONResponse({"success": True, "result": pipeline_dtos[(int(page_number)-1)*int(page_size):(int(page_number))*int(page_size)]})
@router.get("/api/get_result_job/News")
def get_result_job(order = None,text_search = '', page_number = None, page_size = None, start_date : str = '', end_date : str = '', sac_thai : str = '', language_source : str ='',news_letter_id: str = '', authorize: AuthJWT = Depends(),vital:str='',bookmarks:str=''): 
    

    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    #print(user_id)
    try:
        query = {}
        query['$and']=[]

        if start_date != '' and end_date != '':
            start_date = datetime(int(start_date.split('/')[2]), int(start_date.split('/')[1]), int(start_date.split('/')[0]))
            end_date = datetime(int(end_date.split('/')[2]), int(end_date.split('/')[1]), int(end_date.split('/')[0]))
        
            query['$and'].append({'pub_date': {'$gte': start_date, '$lte': end_date}})
        elif start_date != '':
            start_date = datetime(int(start_date.split('/')[2]), int(start_date.split('/')[1]), int(start_date.split('/')[0]))
            query['$and'].append({'pub_date': {'$gte': start_date}})
        elif end_date != '':
            end_date = datetime(int(end_date.split('/')[2]), int(end_date.split('/')[1]), int(end_date.split('/')[0]))
            query['$and'].append({'pub_date': {'$lte': end_date}})

        if sac_thai != '' and sac_thai != 'all':
            query['$and'].append({'data:class_sacthai': sac_thai})
        
        if language_source != '':
            language_source_ = language_source.split(',')
            language_source = []
            for i in language_source_:
                language_source.append(i)
            ls = []
            for i in language_source:
                ls.append({"source_language":i})
            
            query['$and'].append({'$or': ls.copy()})
            
        if news_letter_id != '':
            mongo = MongoRepository().get_one(collection_name='newsletter',filter_spec={'_id':news_letter_id})
            ls = []
            kt_rong = 1
            try:
                for new_id in mongo['news_id']:
                    ls.append({'_id':new_id})
                    kt_rong = 0
                if kt_rong == 0:
                    query['$and'].append({'$or': ls.copy()})
            except:
                if kt_rong == 1:
                    query['$and'].append({'khong_lay_gi':'bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka'})
        elif vital == '1':
            mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
            ls = []
            kt_rong = 1
            try:
                for new_id in mongo['vital_list']:
                    ls.append({'_id':new_id})
                    kt_rong = 0
                if kt_rong == 0:
                    query['$and'].append({'$or': ls.copy()})
            except:
                if kt_rong == 1:
                    query['$and'].append({'khong_lay_gi':'bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka'})

        elif bookmarks == '1':
            mongo = MongoRepository().get_one(collection_name='users',filter_spec={'_id':user_id})
            ls = []
            kt_rong = 1
            try:
                for new_id in mongo['news_bookmarks']:
                    ls.append({'_id':new_id})
                    kt_rong = 0
                if kt_rong == 0:
                    query['$and'].append({'$or': ls.copy()})
            except:
                if kt_rong == 1:
                    query['$and'].append({'khong_lay_gi':'bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka'})
        elif text_search != '':
            tmp = (my_es.search_main(index_name="vosint", query=text_search))
            # print(text_search)
            # print(tmp)
            list_link =[]
            for k in tmp:
                list_link.append({'data:url':k["_source"]["data:url"]})
            if len(list_link) != 0:
                query['$and'].append({'$or': list_link.copy()})
            else:
                query['$and'].append({'khong_lay_gi':'bggsjdgsjgdjádjkgadgưđạgjágdjágdjkgạdgágdjka'})
    except:
        query = {}
    if str(query) == "{'$and': []}":
        query = {}
        
    #print(query)
    return JSONResponse(
        job_controller.get_result_job('News', order, page_number, page_size,filter=query)
    )


# @feature.route('/api/run_one_foreach/<pipeline_id>', methods=['GET','POST'])
# def run_one_foreach(pipeline_id: str):
#     return job_controller.run_one_foreach(pipeline_id)

# @feature.route('/api/test/<pipeline_id>', methods=['GET','POST'])
# def test_only_job(pipeline_id: str):
#     return job_controller.test_only(pipeline_id)
@router.get("/api/get_table")
def get_table(name, id = None,order = None, page_number = None, page_size = None):
    
    query={}
    if id != None:
        query['id']=str(id)


    return JSONResponse(
        job_controller.get_result_job(name, order, page_number, page_size,filter=query)
    )

@router.get("/api/test/{pipeline_id}")
def get_result_job(pipeline_id):
    return JSONResponse(
        job_controller.test_only(pipeline_id))

@router.get("/api/get_log_history/{pipeline_id}")
def get_log_history(pipeline_id: str, order = None, page_number = None, page_size = None):
    return JSONResponse(
        job_controller.get_log_history(pipeline_id, order, page_number, page_size)
    )

@router.get("/api/get_log_history_last/{pipeline_id}")
def get_log_history(pipeline_id: str):
    try:
        return JSONResponse(
            job_controller.get_log_history_last(pipeline_id)['result'][-1]
        )
    except:
        return JSONResponse(
            job_controller.get_log_history_last(pipeline_id)['result']
        )

@router.get("/api/get_log_history_error_or_getnews/{pipeline_id}")
def get_log_history_error_or_getnews(pipeline_id: str, order = None, page_number = None, page_size = None):
    return JSONResponse(
        job_controller.get_log_history_error_or_getnews(
            pipeline_id, order, page_number, page_size
        )
    )
