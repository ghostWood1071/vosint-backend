from common.internalerror import *

from ..common import ActionInfo, ActionType, ParamInfo
from .baseaction import BaseAction


class TestAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="test",
            display_name="Test",
            action_type=ActionType.COMMON,
            readme="Test ...",
            param_infos=[
                ParamInfo(
                    name="by",
                    display_name="Select by",
                    val_type="str",  # val_type='str',
                    default_val="css",
                    validators=["required"],
                ),
                ParamInfo(
                    name="expr",
                    display_name="Expression",
                    val_type="str",
                    default_val="",
                    validators=["required"],
                ),
            ],
            z_index=12,
        )

    def exec_func(self, input_val=None, pipeline_id=None):
        if not input_val:
            raise InternalError(
                ERROR_REQUIRED, params={"code": ["INPUT_URL"], "msg": ["Input URL"]}
            )

        url = input_val
        print("test ...")
        # f= open('abc.txt','a')
        # f.write('test \n')
        # f.close()
        print("abccccccccccccccccccccccccc", pipeline_id)

        # print(type(self.params['by']))
        return self.get_status() + " " + pipeline_id
