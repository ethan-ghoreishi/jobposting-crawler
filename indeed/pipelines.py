# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sys
import psycopg2
from scrapy.utils.python import unicode_to_str
from scrapy.utils.markup import replace_escape_chars, remove_tags
from indeed.settings import SQL 

class IndeedPipeline(object):
    def process_item(self, item, spider):
	
	i = item['summary'][0]
	i = remove_tags(i)
	i = replace_escape_chars(i)
	item['summary'][0] = i

	i = item['job_title'][0]
	i = remove_tags(i)
	i = replace_escape_chars(i)
	item['job_title'][0] = i
	
        return item

class SqlInsert(object):
    def __init__(self):
		db=psycopg2.connect(user=SQL['user'], password=SQL['password'], dbname=SQL['dbname'], host=SQL['host'], port=SQL['port'], charset = "utf8", use_unicode = True)
		self.c=db.cursor()
		
    def process_item(self, item, spider):

	try:
		self.c.execute('''insert into jobs (job_title, link_url, location, company, summary, source, found_date, source_url, source_page_body, crawl_timestamp, crawl_url) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (item['job_title'][0], 
	item['link_url'][0], 
	item['location'][0], 
	item['company'][0],
	item['summary'][0], 
	item['source'][0], 
	item['found_date'][0], 
	item['source_url'], 
	item['source_page_body'],
	item['crawl_timestamp'],
	item['crawl_url']

))
	

            self.c.execute('commit')


        except psycopg2.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)

return item
