from .services import JobService


class JobController:

    def __init__(self):
        self.__job_service = JobService()

    def start_job(self, pipeline_id: str):
        self.__job_service.start_job(pipeline_id)

        return {'success': True}
            

    def start_all_jobs(self, pipeline_ids):
        # Receives request data
        # pipeline_ids = request.args.get('pipeline_ids')

        self.__job_service.start_all_jobs(pipeline_ids)

        return {'success': True}

        

    def stop_job(self, pipeline_id: str):
        self.__job_service.stop_job(pipeline_id)

        return {'success': True}

    def stop_all_jobs(self, pipeline_ids):
        # Receives request data
        # pipeline_ids = request.args.get('pipeline_ids')

        self.__job_service.stop_all_jobs(pipeline_ids)
        return {'success': True}

        

    ### Doan
    def run_only(self, pipeline_id: str):
        result = self.__job_service.run_only(pipeline_id)

        return {'success': True,
                'result': str(result)}

    def get_result_job(self, News, order, page_number, page_size):
        # Receives request data
        # order = request.args.get('order')
        # order = request.args.get('order')
        # page_number = request.args.get('page_number')
        page_number = int(page_number) if page_number is not None else None
        # page_size = request.args.get('page_size')
        page_size = int(page_size) if page_size is not None else None

        # Create sort condition
        order_spec = order.split(',') if order else []

        # Calculate pagination information
        page_number = page_number if page_number else 1
        page_size = page_size if page_size else 20
        pagination_spec = {
            'skip': page_size * (page_number - 1),
            'limit': page_size
        }
        pipeline_dtos, total_records = self.__job_service.get_result_job(News,order_spec=order_spec,
                                                           pagination_spec=pagination_spec)
        for i in pipeline_dtos:
            i['_id'] = str(i['_id'])
        
        return {
                'success': True,
                "total_record":total_records,
                'result': pipeline_dtos
            }
    
    def run_one_foreach(self, pipeline_id: str):
        result = self.__job_service.run_one_foreach(pipeline_id)

        return {
                'result': str(result)
            }
        

    def test_only(self, pipeline_id: str):
        result = self.__job_service.test_only(pipeline_id)

        return {
                'result': result
                
            }
        
    def get_log_history(self, pipeline_id: str, order, page_number, page_size):
        # Receives request data
        # order = request.args.get('order')
        # order = request.args.get('order')
        # page_number = request.args.get('page_number')
        page_number = int(page_number) if page_number is not None else None
        # page_size = request.args.get('page_size')
        page_size = int(page_size) if page_size is not None else None

        # Create sort condition
        order_spec = order.split(',') if order else []

        # Calculate pagination information
        page_number = page_number if page_number else 1
        page_size = page_size if page_size else 20
        pagination_spec = {
            'skip': page_size * (page_number - 1),
            'limit': page_size
        }

        result = self.__job_service.get_log_history(pipeline_id,order_spec=order_spec,
                                                           pagination_spec=pagination_spec)

        return {
                'success': True,
                "total_record":result[1],
                'result': result[0]
            }
        
    
    def get_log_history_error_or_getnews(self, pipeline_id: str, order, page_number, page_size):
        # Receives request data
        # order = request.args.get('order')
        # order = request.args.get('order')
        # page_number = request.args.get('page_number')
        page_number = int(page_number) if page_number is not None else None
        # page_size = request.args.get('page_size')
        page_size = int(page_size) if page_size is not None else None

        # Create sort condition
        order_spec = order.split(',') if order else []

        # Calculate pagination information
        page_number = page_number if page_number else 1
        page_size = page_size if page_size else 20
        pagination_spec = {
            'skip': page_size * (page_number - 1),
            'limit': page_size
        }

        result = self.__job_service.get_log_history_error_or_getnews(pipeline_id,order_spec=order_spec,
                                                           pagination_spec=pagination_spec)

        return {
                'success': True,
                "total_record":result[1],
                'result': result[0]
            }
        
    
    

