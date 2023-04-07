from datetime import datetime

from common.internalerror import *
from models import HBaseRepository, MongoRepository
from models.mongorepository import MongoRepository
from utils import get_time_now_string_y_m_now

from ..common import ActionInfo, ActionType, ParamInfo, SelectorBy
from .baseaction import BaseAction


# from nlp.keyword_extraction.keywords_ext import Keywords_Ext
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
                    # val_type="str",
                    val_type="select",
                    default_val=SelectorBy.CSS,
                    options=SelectorBy.to_list(),
                    validators=["required"],
                ),
                ParamInfo(
                    name="title_expr",
                    display_name="Title Expression",
                    val_type="str",
                    default_val="None",
                    validators=["required_"],
                ),
                ParamInfo(
                    name="author_expr",
                    display_name="Author Expression",
                    val_type="str",
                    default_val="None",
                    validators=["required_"],
                ),
                ParamInfo(
                    name="time",
                    display_name="Time Expression",
                    val_type="pubdate",
                    default_val={
                        "time_expr": "None",
                        "time_format": ["***", ",", "dd", ",", "mm", ",", "yyyy"],
                    },
                    options=["***", "dd", "mm", "yyyy", ",", ".", "/", "_", "-"],
                    validators=["required_"],
                ),
                ParamInfo(
                    name="content_expr",
                    display_name="Content Expression",
                    val_type="str",
                    default_val="None",
                    validators=["required_"],
                ),
            ],
            z_index=4,
        )

    def exec_func(self, input_val=None, **kwargs):
        if not input_val:
            raise InternalError(
                ERROR_REQUIRED, params={"code": ["URL"], "msg": ["URL"]}
            )

        url = str(input_val)
        try:
            url = url.replace("<Page url='", "").replace("'>", "")
        except:
            pass
        # news_info = {}
        # page = input_val
        # by = self.params["by"]
        # time_expr = self.params["time"]['time_expr']
        # time_format = self.params["time"]['time_format']
        # print(time_format)
        # if time_expr != "None" and time_expr !="":
        #     elems = self.driver.select(page, by, time_expr)
        #     if len(elems) > 0:
        #         news_info["data:time"] = self.driver.get_content(elems[0])
        #         #print(news_info["data:time"])

        a, b = MongoRepository().get_many(
            collection_name="News", filter_spec={"data:url": url}
        )
        del a
        if str(b) != "0":
            # print(b)
            print("url already exist")
            return {}

        by = self.params["by"]
        title_expr = self.params["title_expr"]
        author_expr = self.params["author_expr"]
        time_expr = self.params["time"]["time_expr"]
        # time_format = self.params["time"]['time_format']
        time_format = ["***", ",", "dd", "/", "mm", "/", "yyyy", "-", "***"]
        content_expr = self.params["content_expr"]
        news_info = {}

        page = input_val
        check_content = False
        if title_expr != "None" and title_expr != "":
            elems = self.driver.select(page, by, title_expr)
            if len(elems) > 0:
                news_info["data:title"] = self.driver.get_content(elems[0])
        if author_expr != "None" and author_expr != "":
            elems = self.driver.select(page, by, author_expr)
            if len(elems) > 0:
                news_info["data:author"] = self.driver.get_content(elems[0])
        if time_expr != "None" and time_expr != "":
            elems = self.driver.select(page, by, time_expr)
            if len(elems) > 0:
                news_info["data:time"] = self.driver.get_content(elems[0])
                time_string = news_info["data:time"]
                # print(news_info["data:time"])
                format = [",", ".", "/", "_", "-"]
                my_concat = lambda arr: "".join(arr)
                len_time_format = len(time_format)
                time_result = {}
                for i in range(len_time_format):
                    if time_format[i] in format:
                        if i > 0:
                            name_time_format_1 = "time_" + str(time_format[i - 1])
                            # print(time_format[i])
                            # print(time_string)
                            index = time_string.index(
                                time_format[i]
                            )  # split the string at the delimiter
                            # tg = time_string.split(time_format[i])
                            tg = time_string
                            time_string = time_string[index + 1 :]
                            if str(time_format[i - 1]) == "***":
                                continue

                            time_result[f"{name_time_format_1}"] = (
                                f"{tg[:index]}".replace(" ", "")
                                .replace("\n", "")
                                .replace("\t", "")
                            )
                        elif i < (len_time_format - 1):
                            tg = time_string.split(time_format[i])
                            time_string = my_concat(tg[1:])
                        else:
                            pass
                news_info["pub_date"] = ""
                try:
                    if (
                        time_result["time_yyyy"] != "None"
                        and time_result["time_yyyy"] != ""
                    ):
                        news_info["pub_date"] += time_result["time_yyyy"]
                finally:
                    news_info["pub_date"] += "-"
                try:
                    if (
                        time_result["time_mm"] != "None"
                        and time_result["time_mm"] != ""
                    ):
                        news_info["pub_date"] += time_result["time_mm"]
                finally:
                    news_info["pub_date"] += "-"
                try:
                    if (
                        time_result["time_dd"] != "None"
                        and time_result["time_dd"] != ""
                    ):
                        news_info["pub_date"] += time_result["time_dd"]
                except:
                    pass
                finally:
                    try:
                        news_info["pub_date"] = datetime.strptime(
                            str(news_info["pub_date"]), "%Y-%m-%d"
                        )  # .date()
                    except:
                        news_info["pub_date"] = get_time_now_string_y_m_now()

        if content_expr != "None" and content_expr != "":
            elems = self.driver.select(page, by, content_expr)
            if len(elems) > 0:
                news_info["data:content"] = self.driver.get_content(elems[0])
                check_content = True

                # try:
                #     news_info['keywords'] = Keywords_Ext().extracting(document= news_info["data:content"],num_keywords =12)
                # except:
                #     news_info['keywords'] = []

            news_info["data:url"] = url
        if content_expr != "None" and content_expr != "":
            elems = self.driver.select(page, by, content_expr)
            if len(elems) > 0:
                news_info["data:html"] = self.driver.get_html(elems[0])

                tmp_video = self.driver.select(from_elem=page, by="css", expr="figure")
                for i in tmp_video:
                    news_info["data:html"] = news_info["data:html"].replace(
                        self.driver.get_html(i), ""
                    )

        news_info["data:class_chude"] = []
        news_info["data:class_linhvuc"] = []

        news_info["source_name"] = kwargs["source_name"]
        news_info["source_host_name"] = kwargs["source_host_name"]
        news_info["source_language"] = kwargs["source_language"]
        news_info["source_publishing_country"] = kwargs["source_publishing_country"]
        news_info["source_source_type"] = kwargs["source_source_type"]

        if check_content:
            # print('aaaaaaaaaaaaaaaaa')
            try:
                MongoRepository().insert_one(collection_name="News", doc=news_info)

            except:
                print("An error occurred while pushing data to the database!")

        return news_info
