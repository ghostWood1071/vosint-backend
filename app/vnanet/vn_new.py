from datetime import datetime

from fastapi import APIRouter
from playwright.sync_api import sync_playwright

from app.vnanet.service import insert_into_mongodb

router = APIRouter()

@router.get("/fetch-news-in-country")
def fetch_new():
    list_new = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://news.vnanet.vn/?created=7%20day&servicecateid=1&scode=1&qcode=17")

        links = page.query_selector_all("a.spATitle")

        for link in links:
            href = link.get_attribute("href")

            data_id = link.get_attribute("data-id")

            # Retrieve data-service
            data_service = link.get_attribute("data-service")

            # Retrieve timestamp
            timestamp = page.query_selector("span.spADate").inner_text()
            
            # datetime_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": timestamp
            }
            list_new.append(data)
            
        #insert_into_mongodb(list_new)

        browser.close()

    return {"data": list_new}


@router.get("/fetch-news-in-world")
def fetch_new():
    list_new = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://news.vnanet.vn/?created=7%20day&servicecateid=3&scode=1&qcode=17")
        page.wait_for_load_state("networkidle")


        links = page.query_selector_all("a.spATitle")

        for link in links:
            href = link.get_attribute("href")

            data_id = link.get_attribute("data-id")

            # Retrieve data-service
            data_service = link.get_attribute("data-service")

            # Retrieve timestamp
            timestamp = page.query_selector("span.spADate").inner_text()
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": timestamp
            }
            list_new.append(data)

        browser.close()

    return {"data": list_new}

@router.get("/fetch-economics-news-in-country")
def fetch_new():
    list_new = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://news.vnanet.vn/?created=7%20day&servicecateid=10&scode=1&qcode=17")
        page.wait_for_load_state("networkidle")


        links = page.query_selector_all("a.spATitle")

        for link in links:
            href = link.get_attribute("href")

            data_id = link.get_attribute("data-id")

            # Retrieve data-service
            data_service = link.get_attribute("data-service")

            # Retrieve timestamp
            timestamp = page.query_selector("span.spADate").inner_text()
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": timestamp
            }
            list_new.append(data)

        browser.close()

    return {"data": list_new}

@router.get("/fetch-economics-news-in-world")
def fetch_new():
    list_new = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://news.vnanet.vn/?created=7%20day&servicecateid=1000&scode=1&qcode=17")
        page.wait_for_load_state("networkidle")


        links = page.query_selector_all("a.spATitle")

        for link in links:
            href = link.get_attribute("href")

            data_id = link.get_attribute("data-id")

            # Retrieve data-service
            data_service = link.get_attribute("data-service")

            # Retrieve timestamp
            timestamp = page.query_selector("span.spADate").inner_text()
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": timestamp
            }
            list_new.append(data)

        browser.close()

    return {"data": list_new}

@router.get("/fetch-fast-news")
def fetch_new():
    list_new = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://news.vnanet.vn/?created=7%20day&servicecateid=1097&scode=1&qcode=17")
        page.wait_for_load_state("networkidle")


        links = page.query_selector_all("a.spATitle")

        for link in links:
            href = link.get_attribute("href")

            data_id = link.get_attribute("data-id")

            # Retrieve data-service
            data_service = link.get_attribute("data-service")

            # Retrieve timestamp
            timestamp = page.query_selector("span.spADate").inner_text()
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": timestamp
            }
            list_new.append(data)

        browser.close()

    return {"data": list_new}

