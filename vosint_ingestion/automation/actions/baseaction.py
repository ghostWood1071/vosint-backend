from abc import abstractmethod
import time

from common.internalerror import *
from ..common import ActionStatus, ActionInfo
from ..drivers import BaseDriver
from ..storages import BaseStorage
from models import HBaseRepository, MongoRepository

class BaseAction:

    def __init__(self, driver: BaseDriver, storage: BaseStorage, **params):
        self.set_status(ActionStatus.INITIALIZING)

        # Validate input driver
        if not driver:
            raise InternalError(ERROR_REQUIRED,
                                params={
                                    'code': ['DRIVER'],
                                    'msg': ['Driver']
                                })

        # Validate storage
        if not storage:
            raise InternalError(ERROR_REQUIRED,
                                params={
                                    'code': ['STORAGE'],
                                    'msg': ['Storage']
                                })

        # Validate input parameters
        self.__validate_params(**params)

        self.driver = driver
        self.storage = storage
        self.params = params

        self.set_status(ActionStatus.INITIALIZED)

    def __validate_params(self, **params):
        action_info = self.get_action_info()
        for p_info in action_info.param_infos:
            validators = p_info.validators
            # Validate with validators
            if validators:
                for v in validators:
                    if v == 'required':
                        if p_info.name not in params or not params[p_info.name]:
                            raise InternalError(ERROR_REQUIRED,
                                                params={
                                                    'code': [p_info.display_name.upper()],
                                                    'msg': [p_info.display_name]
                                                })

            # Validate value must be in options
            if p_info.options and params[p_info.name] not in p_info.options:
                options = ', '.join(list(map(lambda o: str(o),
                                             p_info.options)))
                raise InternalError(ERROR_NOT_IN,
                                    params={
                                        'code': [p_info.display_name.upper()],
                                        'msg': [p_info.display_name, f'[{options}]']
                                    })

    @classmethod
    @abstractmethod
    def get_action_info(cls) -> ActionInfo:
        raise NotImplementedError()

    def run(self, input_val=None, pipeline_id =None):
        tmp_val = ''
        self.set_status(ActionStatus.RUNNING)
        try:
            res = self.exec_func(input_val,pipeline_id)
            history = self.return_str_status(ActionStatus.COMPLETED)
        except:
            history = self.return_str_status(ActionStatus.ERROR)

        his_log = {}
        his_log['pipeline_id'] = pipeline_id
        his_log['actione'] = f'{self.__class__.__name__}'
        his_log['log'] = history
        his_log['link'] = '' if type(input_val) != str else input_val
        
        MongoRepository().insert_one(collection_name='his_log',doc=his_log)

        # Wait if necessary
        if 'wait' in self.params and self.params['wait']:
            wait_secs = float(self.params['wait'])
            print(f'Waiting {wait_secs}s...')
            time.sleep(wait_secs)

        return res

    @abstractmethod
    def exec_func(self, input_val=None, pipeline_id =None):
        raise NotImplementedError()

    def get_status(self) -> str:
        return self.__status

    def set_status(self, status: str):
        self.__status = status
        print(f'{self.__class__.__name__} ==> {self.__status}')
        #return f'{self.__class__.__name__} ==> {self.__status}'

    def return_str_status(self, status: str):
        return status
