from fastapi import APIRouter
import requests
from fastapi.responses import JSONResponse
import time
from .jobcontroller import JobController
from datetime import datetime
from typing import List
from models import MongoRepository
from fastapi_jwt_auth import AuthJWT
from fastapi.params import Body, Depends

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


@router.post("/api/run_only_job/{pipeline_id}")
def run_only_job(pipeline_id: str, mode_test = True):
    # url = "http://vosint.aiacademy.edu.vn/api/pipeline/Pipeline/api/get_action_infos"
    # requests.get(url)
    # url = "http://vosint.aiacademy.edu.vn/api/pipeline/Pipeline/api/get_pipeline_by_id/"+str(pipeline_id)
    # requests.get(url)
    #time.sleep(5)
    return JSONResponse(job_controller.run_only(pipeline_id, mode_test))


# @router.get("/api/run_only_job/{pipeline_id}")
# def run_only_job(pipeline_id: str, mode_test = True):
#     return JSONResponse(job_controller.run_only(pipeline_id,mode_test))



# @router.get("/api/get_result_job/{News}")
# def get_result_job(News='News', order = None, page_number = None, page_size = None, start_date : str, end_date = str, sac_thai : str, language_source : list):
#     return JSONResponse(
#         job_controller.get_result_job(News, order, page_number, page_size, start_date, end_date, sac_thai, language_source)
#     )

@router.get("/api/get_result_job/News")
def get_result_job(order = None, page_number = None, page_size = None, start_date : str = '', end_date : str = '', sac_thai : str = '', language_source : str ='',news_letter_id: str = '', authorize: AuthJWT = Depends(),vital:str='',bookmarks:str=''): 
    

    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    #print(user_id)
    try:
        query = {}
        query['$and']=[]

        if start_date != '' and end_date != '':
            start_date = datetime(int(start_date.split('/')[2]), int(start_date.split('/')[1]), int(start_date.split('/')[0]))
            end_date = datetime(int(end_date.split('/')[2]), int(end_date.split('/')[1]), int(end_date.split('/')[0]))
        
            query['$and'].append({'pub_date': {'$gt': start_date, '$lt': end_date}})
        elif start_date != '':
            start_date = datetime(int(start_date.split('/')[2]), int(start_date.split('/')[1]), int(start_date.split('/')[0]))
            query['$and'].append({'pub_date': {'$gt': start_date}})
        elif end_date != '':
            end_date = datetime(int(end_date.split('/')[2]), int(end_date.split('/')[1]), int(end_date.split('/')[0]))
            query['$and'].append({'pub_date': {'$lt': end_date}})

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
@router.get("/api/test/{pipeline_id}")
def get_result_job(pipeline_id):
    return JSONResponse(
        job_controller.test_only(pipeline_id))

@router.get("/api/get_log_history/{pipeline_id}")
def get_log_history(pipeline_id: str, order = None, page_number = None, page_size = None):
    return JSONResponse(
        job_controller.get_log_history(pipeline_id, order, page_number, page_size)
    )


@router.get("/api/get_log_history_error_or_getnews/{pipeline_id}")
def get_log_history_error_or_getnews(pipeline_id: str, order = None, page_number = None, page_size = None):
    return JSONResponse(
        job_controller.get_log_history_error_or_getnews(
            pipeline_id, order, page_number, page_size
        )
    )
