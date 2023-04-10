from ...common import ActionInfo, ActionType, ParamInfo
from ..baseaction import BaseAction


class URLInputAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="url_input",
            display_name="URL Input",
            action_type=ActionType.INPUT,
            readme="Đầu vào địa chỉ URL",
            param_infos=[
                ParamInfo(
                    name="url",
                    display_name="URL",
                    val_type="str",
                    default_val="",
                    validators=["required"],
                ),
                ParamInfo(#check URL input .run only url
                    name="source",
                    display_name="Nguồn",
                    val_type="source",  # val_type='str',
                    default_val='',
                    options='',
                    validators=["required_"]
                )
                
            ],
            z_index=0,
        )

    def exec_func(self, input_val=None, **kwargs):
        return self.params["url"]
