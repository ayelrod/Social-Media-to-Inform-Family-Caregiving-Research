#!/bin/sh
pip install python3
pip install scrapy
pip install dnspython
pip install pymongo
cd ./web_scraping/web_scraping

scrapy crawl als_past_caregivers

scrapy crawl als

scrapy crawl alz

# scrapy crawl ac
