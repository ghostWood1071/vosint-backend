from common.internalerror import *

from ..common import ActionInfo, ActionType, ParamInfo
from .baseaction import BaseAction


class ClickAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="click",
            display_name="Click",
            action_type=ActionType.COMMON,
            readme="Click một thành phần",
            z_index=7,
        )

    def exec_func(self, input_val=None, pipeline_id=None):
        if not input_val:
            raise InternalError(
                ERROR_REQUIRED, params={"code": ["FROM_ELEM"], "msg": ["From element"]}
            )

        from_elem = input_val
        # attr_name = self.params['attr_name']
        return self.driver.click(from_elem)
