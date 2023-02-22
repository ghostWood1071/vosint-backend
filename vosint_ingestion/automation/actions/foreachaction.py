from common.internalerror import *

from ..common import ActionInfo, ActionType, ParamInfo
from .baseaction import BaseAction
from .clickaction import ClickAction
from .getattraction import GetAttrAction
from .getnewsinfoaction import GetNewsInfoAction
from .geturlsaction import GetUrlsAction
from .gotoaction import GotoAction
from .login import LoginAction
from .selectaction import SelectAction
from .test import TestAction


def get_action_class(name: str):
    action_cls = (
        GotoAction
        if name == "goto"
        else GetUrlsAction
        if name == "get_urls"
        else GetNewsInfoAction
        if name == "get_news_info"
        else SelectAction
        if name == "select"
        else GetAttrAction
        if name == "get_attr"
        else ForeachAction
        if name == "foreach"
        else ClickAction
        if name == "click"
        else TestAction
        if name == "test"
        else LoginAction
        if name == "login"
        else None
    )
    if action_cls is None:
        raise InternalError(
            ERROR_NOT_FOUND,
            params={"code": [f"{name.upper()}_ACTION"], "msg": [f"{name} action"]},
        )

    return action_cls


class ForeachAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="foreach",
            display_name="Foreach",
            action_type=ActionType.COMMON,
            readme="Cấu trúc lặp cho mỗi phần tử",
            param_infos=[
                ParamInfo(
                    name="actions",
                    display_name="List of actions",
                    val_type="list",
                    default_val=[],
                    validators=["required"],
                )
            ],
            z_index=6,
        )

    def exec_func(self, input_val=None, pipeline_id=None):
        actions = self.params["actions"]
        flatten = False if "flatten" not in self.params else self.params["flatten"]

        # Run foreach actions
        res = []
        if input_val is not None:
            for val in input_val:
                if flatten == False:
                    res.append(self.__run_actions(actions, val, pipeline_id))
                else:
                    res += self.__run_actions(actions, val, pipeline_id)
                # if self.params['test_pipeline'] == 'True':
                #     break
        return res

    def __run_actions(self, actions: list[dict], input_val, pipeline_id=None):
        tmp_val = input_val
        for act in actions:
            params = act["params"] if "params" in act else {}
            action = get_action_class(act["name"])(self.driver, self.storage, **params)
            tmp_val = action.run(tmp_val, pipeline_id)
        return tmp_val
