from playwright.sync_api import sync_playwright
import time
from ..common import SelectorBy
from .basedriver import BaseDriver


class PlaywrightDriver(BaseDriver):
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.driver = self.playwright.chromium.launch(channel='chrome')
        self.page = self.driver.new_page()

    def destroy(self):
        self.driver.close()
        self.playwright.stop()

    def goto(self, url: str):
        self.page.goto(url)
        return self.page

    def select(self, from_elem, by: str, expr: str):
        by = self.__map_selector_by(by)
        elems = from_elem.locator(f'{by}{expr}')
        # Cast elems to list
        elems = [elems.nth(i) for i in range(elems.count())]
        return elems

    def get_attr(self, from_elem, attr_name: str):
        return from_elem.get_attribute(attr_name)

    def get_content(self, from_elem) -> str:
        return from_elem.inner_text()

    def click(self, from_elem):
        from_elem.click()

    #TODO DoanCT: Bo sung scroll, sendkey
    def scroll(self, from_elem, value: int):
        for i in range(value): #make the range as long as needed
            self.page.mouse.wheel(0, 15000)
            time.sleep(1)

    def sendkey(self, from_elem , value: str):
        from_elem.type(value)



    def fill(self, from_elem, value: str):
        from_elem.fill(value)

    def __map_selector_by(self, selector_by: str) -> str:
        return 'xpath=' if selector_by == SelectorBy.XPATH else 'css='
