from common.internalerror import *
from models import HBaseRepository, MongoRepository

from ..common import ActionInfo, ActionType, ParamInfo, SelectorBy
from .baseaction import BaseAction


class GetNewsInfoAction(BaseAction):
    @classmethod
    def get_action_info(cls) -> ActionInfo:
        return ActionInfo(
            name="get_news_info",
            display_name="Get News Infomation",
            action_type=ActionType.COMMON,
            readme="Lấy thông tin bài viết",
            param_infos=[
                ParamInfo(
                    name="by",
                    display_name="Select by",
                    val_type="str",
                    default_val=SelectorBy.CSS,
                    options=SelectorBy.to_list(),
                    validators=["required"],
                ),
                ParamInfo(
                    name="title_expr",
                    display_name="Title Expression",
                    val_type="str",
                    default_val="",
                    validators=["required"],
                ),
                ParamInfo(
                    name="author_expr",
                    display_name="Author Expression",
                    val_type="str",
                    default_val="",
                    validators=["required"],
                ),
                ParamInfo(
                    name="time_expr",
                    display_name="Time Expression",
                    val_type="str",
                    default_val="",
                    validators=["required"],
                ),
                ParamInfo(
                    name="content_expr",
                    display_name="Content Expression",
                    val_type="str",
                    default_val="",
                    validators=["required"],
                ),
                #   ParamInfo(name='name',
                #             display_name='Name',
                #             val_type='str',
                #             default_val='News',
                #             validators=['required'])
            ],
            z_index=4,
        )

    def exec_func(self, input_val=None, pipeline_id=None):
        if not input_val:
            raise InternalError(
                ERROR_REQUIRED, params={"code": ["URL"], "msg": ["URL"]}
            )

        url = input_val
        by = self.params["by"]
        title_expr = self.params["title_expr"]
        author_expr = self.params["author_expr"]
        time_expr = self.params["time_expr"]
        content_expr = self.params["content_expr"]

        # Crawl news information
        news_info = {}
        page = self.driver.goto(url)
        elems = self.driver.select(page, by, title_expr)
        if len(elems) > 0:
            news_info["data:title"] = self.driver.get_content(elems[0])
        elems = self.driver.select(page, by, author_expr)
        if len(elems) > 0:
            news_info["data:author"] = self.driver.get_content(elems[0])
        elems = self.driver.select(page, by, time_expr)
        if len(elems) > 0:
            news_info["data:time"] = self.driver.get_content(elems[0])
        elems = self.driver.select(page, by, content_expr)
        if len(elems) > 0:
            news_info["data:content"] = self.driver.get_content(elems[0])
        news_info["data:url"] = url
        news_info["data:class_chude"] = []
        news_info["data:class_linhvuc"] = []

        # Put news information into the database
        if news_info:
            try:
                # news_info['data:url'] = url
                # self.storage.put('news', news_info, row_key='data:url')
                # try:
                # results={
                # 'id_pipeline' : str(id),
                # 'time' : get_time_now_string(),
                # 'result' : str(result)}
                MongoRepository().insert_one(collection_name="News", doc=news_info)
            # except:
            #     print('mongo error insert')

            except:
                print("An error occurred while pushing data to the database!")

        return news_info
