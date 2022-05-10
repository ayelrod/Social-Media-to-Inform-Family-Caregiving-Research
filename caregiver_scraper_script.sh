#!/bin/sh
pip install python3
pip install scrapy
pip install dnspython
pip install pymongo
cd ./web_scraping/web_scraping

scrapy crawl als_past_caregivers & sleep 300 ; kill $!

scrapy crawl als & sleep 300 ; kill $!

scrapy crawl alz & sleep 300 ; kill $!

# scrapy crawl ac
