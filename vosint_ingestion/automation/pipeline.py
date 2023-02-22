from common.internalerror import *

from .actions import URLInputAction, get_action_class
from .common import ActionType
from .drivers import BaseDriver
from .storages import BaseStorage
from .utils import get_action_info


class Pipeline:
    def __init__(
        self,
        driver: BaseDriver,
        storage: BaseStorage,
        actions: list[dict],
        pipeline_id=None,
    ):
        if not driver:
            raise InternalError(
                ERROR_REQUIRED, params={"code": ["DRIVER"], "msg": ["Driver"]}
            )

        if not storage:
            raise InternalError(
                ERROR_REQUIRED, params={"code": ["STORAGE"], "msg": ["Storage"]}
            )

        if not actions:
            raise InternalError(
                ERROR_REQUIRED,
                params={"code": ["ACTION_LIST"], "msg": ["List of actions"]},
            )

        # Validate the first action must be input type
        first_action = actions[0]
        if "name" not in first_action or not first_action["name"]:
            raise InternalError(
                ERROR_REQUIRED,
                params={
                    "code": ["FIRST_ACTION_NAME"],
                    "msg": ["The first action name"],
                },
            )

        first_action_info = get_action_info(first_action["name"])
        if first_action_info is None:
            raise InternalError(
                ERROR_NOT_FOUND,
                params={
                    "code": [f'{first_action["name"].upper()}_ACTION'],
                    "msg": [f'{first_action["name"]} action'],
                },
            )

        if first_action_info["action_type"] != ActionType.INPUT:
            raise InternalError(
                ERROR_NOT_INPUT,
                params={"code": ["FIRST_ACTION"], "msg": ["The first action"]},
            )

        self.__driver = driver
        self.__storage = storage
        self.__first_action = first_action
        self.__common_actions = actions[1:]
        self.pipeline_id = pipeline_id

    def run(self):
        # Run first action
        url = self.__first_action["params"]["url"]
        action = URLInputAction(self.__driver, self.__storage, url=url)
        input_val = action.run(pipeline_id=self.pipeline_id)

        # Run from 2nd action
        for act in self.__common_actions:
            params = act["params"] if "params" in act else {}
            action = get_action_class(act["name"])(
                self.__driver, self.__storage, **params
            )
            input_val = action.run(input_val, self.pipeline_id)

        # Destroy driver after work done
        self.__driver.destroy()

        return input_val
