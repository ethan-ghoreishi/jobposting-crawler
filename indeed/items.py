# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class IndeedItem(Item):
    # define the fields for your item here like:
    # name = Field()
    job_title = Field()
    link_url = Field()
    location = Field()
    company = Field()
    summary = Field()
#    src = Field()
    found_date = Field()
    source_url = Field()
    source_page_body = Field()
    crawl_url = Field()
    crawl_timestamp = Field()
pass
