# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from Zoldesk.items import ZoldeskItem

class ZoldeskspiderSpider(CrawlSpider):
    name = 'Zoldeskspider'
    allowed_domains = ['desk.zol.com.cn']
    start_urls = ['https://desk.zol.com.cn/pc/1.html']
    base_url="http://desk.zol.com.cn"
    rules = (
        Rule(LinkExtractor(allow=r'http://desk\.zol\.com\.cn/pc/\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'http://desk\.zol\.com\.cn/bizhi/.+\.html'), callback="parse_item", follow=False),
    )

    def parse_item(self, response):

        picurllist= response.xpath(".//dd[@id='tagfbl']/a/@href").extract()[0:-2]
        for picurl in picurllist:
            picweburl=(self.base_url+picurl)
            yield scrapy.Request(
            picweburl,
            callback=self.imagedetail
            )
    def imagedetail(self,response):

        src=response.xpath(".//body/img/@src").extract_first().split()
        images="pic"
        item=ZoldeskItem(image_urls=src,images=images)
        yield item
