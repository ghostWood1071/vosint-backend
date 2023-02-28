import datetime
import json

from automation import Session
from common.internalerror import *
from features.pipeline.services import PipelineService
from logger import Logger
from scheduler import Scheduler
from utils import get_time_now_string

from models import HBaseRepository, MongoRepository


def start_job(actions: list[dict], pipeline_id=None):
    session = Session(
        driver_name="playwright",
        storage_name="hbase",
        actions=actions,
        pipeline_id=pipeline_id,
    )
    # print('aaaaaaaaaaaa',pipeline_id)
    return session.start()


class JobService:
    def __init__(self):
        self.__pipeline_service = PipelineService()
        self.__mongo_repo = MongoRepository()

    def run_only(self, id: str):
        pipeline_dto = self.__pipeline_service.get_pipeline_by_id(id)
        session = Session(
            driver_name="playwright",
            storage_name="hbase",
            actions=pipeline_dto.schema,
            pipeline_id=id,
        )
        result = session.start()
        # try:
        #     results={
        #     'id_pipeline' : str(id),
        #     'time' : get_time_now_string(),
        #     'result' : str(result)}
        #     self.__mongo_repo.insert_one(collection_name='Test',doc=results)
        # except:
        #     print('mongo error insert')
        return result  # pipeline_dto.schema #

    def get_result_job(self, News, order_spec, pagination_spec):
        results = self.__mongo_repo.get_many_News(
            News, order_spec=order_spec, pagination_spec=pagination_spec
        )
        # results['_id'] = str(results['_id'])
        return results  # pipeline_dto.schema #

    def get_log_history(self, id: str, order_spec, pagination_spec):
        results = self.__mongo_repo.get_many_his_log(
            "his_log",
            {"pipeline_id": id},
            order_spec=order_spec,
            pagination_spec=pagination_spec,
        )

        return results

    def get_log_history_error_or_getnews(self, id: str, order_spec, pagination_spec):
        results = self.__mongo_repo.get_many_his_log(
            "his_log",
            {
                "$and": [
                    {"pipeline_id": id},
                    {"$or": [{"actione": "GetNewsInfoAction"}, {"log": "error"}]},
                ]
            },
            order_spec=order_spec,
            pagination_spec=pagination_spec,
        )

        return results

    def run_one_foreach(self, id: str):
        pipeline_dto = self.__pipeline_service.get_pipeline_by_id(id)
        session = Session(
            driver_name="playwright",
            storage_name="hbase",
            # flag = 0,
            actions=pipeline_dto.schema,
        )
        return session.start()  # pipeline_dto.schema #

    def test_only(self, id: str):
        pipeline_dto = self.__pipeline_service.get_pipeline_by_id(id)
        # session = Session(driver_name='playwright',
        #           storage_name='hbase',
        #           actions=pipeline_dto.schema)
        return pipeline_dto.schema  #

    def start_job(self, id: str):
        pipeline_dto = self.__pipeline_service.get_pipeline_by_id(id)
        if not pipeline_dto:
            raise InternalError(
                ERROR_NOT_FOUND,
                params={"code": ["PIPELINE"], "msg": [f"pipeline with id: {id}"]},
            )

        if not pipeline_dto.enabled:
            raise InternalError(
                ERROR_NOT_FOUND,
                params={"code": ["PIPELINE"], "msg": [f"Pipeline with id: {id}"]},
            )

        pipeline_id = str(id)
        Scheduler.instance().add_job(
            id, start_job, pipeline_dto.cron_expr, args=[pipeline_dto.schema, id]
        )

    def start_all_jobs(self, pipeline_ids: list[str] = None):
        # Split pipeline_ids from string to list of strings
        pipeline_ids = pipeline_ids.split(",") if pipeline_ids else None

        enabled_pipeline_dtos = self.__pipeline_service.get_pipelines_for_run(
            pipeline_ids
        )

        def func(actions):
            def _():
                session = Session(
                    driver_name="playwright", storage_name="hbase", actions=actions
                )
                session.start()

            return _

        for pipeline_dto in enabled_pipeline_dtos:
            try:
                Scheduler.instance().add_job(
                    pipeline_dto._id, func(pipeline_dto.schema), pipeline_dto.cron_expr
                )
            except InternalError as error:
                Logger.instance().error(str(error))

    def stop_job(self, id: str):
        Scheduler.instance().remove_job(id)

    def stop_all_jobs(self, pipeline_ids: list[str] = None):
        # Split pipeline_ids from string to list of strings
        pipeline_ids = pipeline_ids.split(",") if pipeline_ids else None

        enabled_pipeline_dtos = self.__pipeline_service.get_pipelines_for_run(
            pipeline_ids
        )

        for pipeline_dto in enabled_pipeline_dtos:
            try:
                Scheduler.instance().remove_job(pipeline_dto._id)
            except InternalError as error:
                Logger.instance().error(str(error))
