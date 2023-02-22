from common.internalerror import *
from ..common import ActionInfo, ParamInfo, ActionType
from .baseaction import BaseAction


class ScrollAction(BaseAction):

    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(name='scroll',
                          display_name='Scroll',
                          action_type=ActionType.COMMON,
                          readme='Cuộn trang web',
                          param_infos=[
                              ParamInfo(name='number_scroll',
                                        display_name='Scroll page number',
                                        val_type='str',
                                        default_val='1',
                                        validators=['required'])
                          ],
                          z_index=8)

    def exec_func(self, input_val=None, pipeline_id =None):
        if not input_val:
            raise InternalError(ERROR_REQUIRED,
                                params={
                                    'code': ['FROM_ELEM'],
                                    'msg': ['From element']
                                })

        from_elem = input_val
        number_scroll = self.params['number_scroll']
        return self.driver.scoll(from_elem, number_scroll)