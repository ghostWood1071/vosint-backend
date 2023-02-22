# from flask import Blueprint

# from .jobcontroller import JobController


# feature = Blueprint('Job', __name__)
# job_controller = JobController()


# @feature.route('/api/start_job/<pipeline_id>', methods=['POST'])
# def start_job(pipeline_id: str):
#     return job_controller.start_job(pipeline_id)


# @feature.route('/api/start_all_jobs', methods=['POST'])
# def start_all_jobs():
#     return job_controller.start_all_jobs()


# @feature.route('/api/stop_job/<pipeline_id>', methods=['POST'])
# def stop_job(pipeline_id: str):
#     return job_controller.stop_job(pipeline_id)


# @feature.route('/api/stop_all_jobs', methods=['POST'])
# def stop_all_jobs():
#     return job_controller.stop_all_jobs()

# @feature.route('/api/run_only_job/<pipeline_id>', methods=['GET','POST'])
# def run_only_job(pipeline_id: str):
#     return job_controller.run_only(pipeline_id)

# @feature.route('/api/get_result_job/<News>', methods=['GET','POST'])
# def get_result_job(News):
#     return job_controller.get_result_job(News)

# @feature.route('/api/run_one_foreach/<pipeline_id>', methods=['GET','POST'])
# def run_one_foreach(pipeline_id: str):
#     return job_controller.run_one_foreach(pipeline_id)

# @feature.route('/api/test/<pipeline_id>', methods=['GET','POST'])
# def test_only_job(pipeline_id: str):
#     return job_controller.test_only(pipeline_id)

# @feature.route('/api/get_log_history/<pipeline_id>', methods=['GET','POST'])
# def get_log_history(pipeline_id: str):
#     return job_controller.get_log_history(pipeline_id)

# @feature.route('/api/get_log_history_error_or_getnews/<pipeline_id>', methods=['GET','POST'])
# def get_log_history_error_or_getnews(pipeline_id: str):
#     return job_controller.get_log_history_error_or_getnews(pipeline_id)
