# -*- coding: utf-8 -*-
#from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.http import Request
import time
import sys
from indeed.items import IndeedItem
import scrapy


class IndeedJpostingSpider(CrawlSpider):
    name = 'indeed_jposting'
    allowed_domains = ['indeed.com']
    start_urls = ["http://www.indeed.com/jobs?q=linux&l=Chicago&sort=date?",]
#    start_urls = ["https://www.indeed.com/jobs?q=PhD&l=united+states&rq=1&fromage=last"]

    rules = ( 
		Rule(LinkExtractor(allow=('/jobs.q=linux&l=Chicago&sort=date$','q=linux&l=Chicago&sort=date&start=[0-9]+$',),deny=('/my/mysearches', '/preferences', '/advanced_search','/my/myjobs')), callback='parse_item', follow=True),

    	)
    print('rule passed')

#    rules = (Rule (LinkExtractor(restrict_xpaths = ('//span[@class="np"]')), callback = "parse_item", follow = True),)

    def parse_next_site(self, response):
#        item = []
        item = response.request.meta['item']
        item['source_url'] = response.url
        item['source_page_body'] = response.body
        item['crawl_timestamp'] =  time.strftime('%Y-%m-%d %H:%M:%S')
        print(item)
        
        return item 


    def parse_item(self, response):
        self.log('\n Crawling  %s\n' % response.url)
        hxs = Selector(response)
#        sites = hxs.select("//div[@class='row ' or @class='row lastRow']")
        sites = hxs.xpath("//div[@class='  row  result' or @class='lastRow  row  result' or @class='row sjlast result']")
	#sites = hxs.select("//div[@class='row ']")
        items = []
        for site in sites:
            item = IndeedItem(company='none')
	
            item['job_title'] = site.xpath('h2/a/@title').extract()
            link_url= site.xpath('h2/a/@href').extract()
            item['link_url'] = link_url
            item['crawl_url'] = response.url
            item['location'] = site.xpath("span[@class='location']/text()").extract()

	    # Not all entries have a company
            if site.xpath("span[@class='company']/text()").extract() == []:
                item['company'] = [u'']
            else:
                item['company'] = site.xpath("span[@class='company']//text()").extract()
                item['summary'] = site.xpath("//table/tr/td/span[@class='summary']").extract()
                item['src'] = site.xpath("table/tr/td/span[@class='source']/text()").extract()
                item['found_date'] = site.xpath("table/tr/td//span[@class='date']/text()").extract()
		#item['source_url'] = self.get_source(link_url)
                request = Request("http://www.indeed.com" + item['link_url'][0], callback=self.parse_next_site)
                request.meta['item'] = item
                yield request

                items.append(item)
        print(items)
        return items

			
SPIDER=IndeedJpostingSpider()

