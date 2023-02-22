from .drivers import DriverFactory
from .storages import StorageFactory
from .pipeline import Pipeline


class Session:
    def __init__(self, driver_name: str, storage_name: str, actions: list[dict] ,pipeline_id = None):
        self.__driver = DriverFactory(driver_name)
        self.__storage = StorageFactory(storage_name)
        self.__pipeline = Pipeline(self.__driver, self.__storage, actions, pipeline_id)

    def start(self):
        print('Started session!')
        res = self.__pipeline.run()
        print('Finished session!')

        return res
