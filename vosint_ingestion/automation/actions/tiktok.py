from ..common import ActionInfo, ActionType, ParamInfo
from .baseaction import BaseAction


class TiktokAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="tiktok",
            display_name="Tiktok",
            action_type=ActionType.COMMON,
            readme="tiktok",
            param_infos=[
                ParamInfo(
                    name="link_person",
                    display_name="cookie",
                    val_type="str",
                    default_val="",
                    validators=["required_"],
                )
            ],
            z_index=14,
        )

    def exec_func(self, input_val=None, **kwargs):
        pass