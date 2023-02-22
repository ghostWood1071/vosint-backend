import uuid
from datetime import datetime

import pytz
import unidecode


def get_time_now_string(
    tz: str = "Asia/Ho_Chi_Minh", fmt: str = "%Y/%m/%d %H:%M:%S"
) -> str:
    return datetime.now(pytz.timezone(tz)).strftime(fmt)


def gen_id(length: int = 12) -> str:
    return str(uuid.uuid4().hex[-length:])


def norm_text(text: str) -> str:
    text_lower = text.lower()
    text_removed_accent = unidecode.unidecode(text_lower)
    return text_removed_accent
