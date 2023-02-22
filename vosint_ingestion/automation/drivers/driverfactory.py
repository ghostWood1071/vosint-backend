from common.internalerror import *

from .playwrightdriver import PlaywrightDriver


class DriverFactory:
    def __new__(cls, name: str):
        driver_cls = PlaywrightDriver if name == "playwright" else None
        if driver_cls is None:
            raise InternalError(
                ERROR_NOT_FOUND, params={"code": ["DRIVER"], "msg": [f"{name} driver"]}
            )

        return driver_cls()
