from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .jobcontroller import JobController

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
def run_only_job(pipeline_id: str):
    return JSONResponse(job_controller.run_only(pipeline_id))


@router.get("/api/run_only_job/{pipeline_id}")
def run_only_job(pipeline_id: str):
    return JSONResponse(job_controller.run_only(pipeline_id))


@router.get("/api/get_result_job/{News}")
def get_result_job(News, order, page_number, page_size):
    return JSONResponse(
        job_controller.get_result_job(News, order, page_number, page_size)
    )


# @feature.route('/api/run_one_foreach/<pipeline_id>', methods=['GET','POST'])
# def run_one_foreach(pipeline_id: str):
#     return job_controller.run_one_foreach(pipeline_id)

# @feature.route('/api/test/<pipeline_id>', methods=['GET','POST'])
# def test_only_job(pipeline_id: str):
#     return job_controller.test_only(pipeline_id)


@router.get("/api/get_log_history/{pipeline_id}")
def get_log_history(pipeline_id: str, order, page_number, page_size):
    return JSONResponse(
        job_controller.get_log_history(pipeline_id, order, page_number, page_size)
    )


@router.get("/api/get_log_history_error_or_getnews/{pipeline_id}")
def get_log_history_error_or_getnews(pipeline_id: str, order, page_number, page_size):
    return JSONResponse(
        job_controller.get_log_history_error_or_getnews(
            pipeline_id, order, page_number, page_size
        )
    )
