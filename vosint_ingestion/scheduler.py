from typing import Callable

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from common.internalerror import *
from core.config import settings
from apscheduler.jobstores.mongodb import MongoDBJobStore
import utils


class Scheduler:
    __instance = None

    def __init__(self):
        if Scheduler.__instance is not None:
            raise InternalError(
                ERROR_SINGLETON_CLASS,
                params={
                    "code": [self.__class__.__name__.upper()],
                    "msg": [self.__class__.__name__],
                },
            )

        mongo_config = {
            "host": settings.mong_host,
            "port": settings.mongo_port,
            "username": settings.mongo_username,
            "password": settings.mongo_passwd,
            "database": settings.mongo_db_name,
            "collection": "jobstore",
        }
        jobstore = {"default": MongoDBJobStore(**mongo_config)}
        self.__bg_scheduler = BackgroundScheduler(jobstores=jobstore)
        self.__bg_scheduler.start()

        Scheduler.__instance = self

    @staticmethod
    def instance():
        """Static access method."""
        if Scheduler.__instance is None:
            Scheduler()
        return Scheduler.__instance

    def add_job(self, id: str, func: Callable, cron_expr: str, args: list = []):
        # print('args..............',args)
        self.__bg_scheduler.add_job(
            id=id, func=func, args=args, trigger=CronTrigger.from_crontab(cron_expr)
        )

    def remove_job(self, id: str):
        self.__bg_scheduler.remove_job(id)

    def get_jobs(self) -> list:
        jobs = [job.id for job in self.__bg_scheduler.get_jobs()]
        return jobs

    def add_job_interval(
        self,
        id: str,
        func: Callable,
        interval: int,
        args: list = [],
        next_run_time=None,
    ):
        self.__bg_scheduler.add_job(
            id=id,
            func=func,
            args=args,
            trigger="interval",
            seconds=interval,
            next_run_time=next_run_time,
        )

    def add_job_crawl_ttxvn(self):
        self.__bg_scheduler.add_job(
            id="crawttxvnnews",
            func=utils.crawl_ttxvn_func,
            trigger=CronTrigger.from_crontab("0 * * * *"),
        )
