from datetime import datetime

from fastapi import APIRouter
from playwright.sync_api import sync_playwright
from pymongo import MongoClient
from core.config import settings

router = APIRouter()

@router.get("/fetch-news-in-country")
def fetch_new_in_country():
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
            
            datetime_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": datetime_obj
            }
            list_new.append(data)
            
        insert_into_mongodb(list_new)
        
    return {"data": list_new}


@router.get("/fetch-news-in-world")
def fetch_new_in_world():
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
            
            datetime_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": datetime_obj
            }
            list_new.append(data)
            
        insert_into_mongodb_2(list_new)

    return {"data": list_new}

@router.get("/fetch-economics-news-in-country")
def fetch_new_economics_news_in_country():
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
            
            datetime_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": datetime_obj
            }
            list_new.append(data)
            
        insert_into_mongodb_3(list_new)
        
    return {"data": list_new}

@router.get("/fetch-economics-news-in-world")
def fetch_newe_conomics_news_in_world():
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
            
            datetime_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
            
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": datetime_obj
            }
            list_new.append(data)
            
        insert_into_mongodb_4(list_new)

    return {"data": list_new}

@router.get("/fetch-fast-news")
def fetch_fast_new():
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
            
            datetime_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
                   
            data = {
                "href": href,
                "data-id": data_id,
                "data-service": data_service,
                "date": datetime_obj
            }
            list_new.append(data)
        
        insert_into_mongodb_5(list_new)

    return {"data": list_new}


def insert_into_mongodb(data):
    client = MongoClient(settings.MONGO_DETAILS)
    database = client.vosint_db
    collection = database.News_vnanet
    collection.insert_many(data)

def insert_into_mongodb_2(data):
    client = MongoClient(settings.MONGO_DETAILS)
    database = client.vosint_db
    collection = database.News_vnanet
    collection.insert_many(data)

def insert_into_mongodb_3(data):
    client = MongoClient(settings.MONGO_DETAILS)
    database = client.vosint_db
    collection = database.News_vnanet
    collection.insert_many(data)

def insert_into_mongodb_4(data):
    client = MongoClient(settings.MONGO_DETAILS)
    database = client.vosint_db
    collection = database.News_vnanet
    collection.insert_many(data)

def insert_into_mongodb_5(data):
    client = MongoClient(settings.MONGO_DETAILS)
    database = client.vosint_db
    collection = database.News_vnanet
    collection.insert_many(data)
