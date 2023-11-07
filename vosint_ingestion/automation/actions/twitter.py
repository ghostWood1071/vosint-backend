from ..common import ActionInfo, ActionType, ParamInfo
from .baseaction import BaseAction


class TwitterAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="twitter",
            display_name="Twitter",
            action_type=ActionType.COMMON,
            readme="twitter",
            param_infos=[
                ParamInfo(
                    name="link_person",
                    display_name="Link đối tượng theo dõi",
                    val_type="str",
                    default_val="",
                    validators=["required_"],
                ),
                ParamInfo(
                    name="type",
                    display_name="Đối tượng",
                    val_type="select",
                    default_val="",
                    options = ['account'],
                    validators=["required_"],
                )
            ],
            z_index=15,
        )

    def exec_func(self, input_val=None, **kwargs):
        pass
