from datetime import timedelta
from bson.objectid import ObjectId
from datetime import datetime

# from models import MongoRepository
# from models import MongoRepository
from vosint_ingestion.models.mongorepository import MongoRepository


def status_source_news(day_space: int = 3, start_date=None, end_date=None):
    now = datetime.now()
    now = now.today() - timedelta(days=day_space)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=day_space + 1, seconds=-1)

    if start_date:
        start_of_day = datetime(
            int(start_date.split("/")[2]),
            int(start_date.split("/")[1]),
            int(start_date.split("/")[0]),
        )

    if end_date:
        end_date = datetime(
            int(end_date.split("/")[2]),
            int(end_date.split("/")[1]),
            int(end_date.split("/")[0]),
        )
        end_of_day = end_date.replace(hour=23, minute=59, second=59)

    start_of_day = start_of_day.strftime("%Y/%m/%d %H:%M:%S")
    end_of_day = end_of_day.strftime("%Y/%m/%d %H:%M:%S")

    list_hist = MongoRepository().aggregate(
        "his_log",
        [
            {
                "$match": {
                    "created_at": {"$gte": start_of_day, "$lte": end_of_day},
                }
            }
        ],
    )

    list_pipelines = MongoRepository().aggregate("pipelines", [])

    result = {
        "normal": 0,
        "error": 0,
        "unknown": 0,
    }

    if list_pipelines:
        for pipeline in list_pipelines:
            if pipeline["enabled"]:
                id = pipeline["_id"]

                is_completed = False
                is_unknown = True
                for his in list_hist:
                    if ObjectId(his["pipeline_id"]) == id:
                        is_unknown = False
                        if his["log"] == "completed":
                            is_completed = True
                            result["normal"] += 1
                            break

                if not is_completed and not is_unknown:
                    result["error"] += 1
                elif is_unknown:
                    result["unknown"] += 1

            else:
                result["unknown"] += 1
        result["last_update"] = datetime.now()
        in_db = MongoRepository().get_many("err_source_statistic", {})
        if in_db[1] == 0:
            MongoRepository().insert_one("err_source_statistic", result)
        else:
            MongoRepository().update_many(
                "err_source_statistic", {"_id": in_db[0][0]["_id"]}, {"$set": result}
            )
    return result
