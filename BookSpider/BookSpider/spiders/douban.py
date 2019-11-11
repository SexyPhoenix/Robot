# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib.parse import urljoin
from BookSpider.items import BookspiderItem
from scrapy.loader import ItemLoader

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/神经网络'] # 神经网络

    def parse(self, response):
     
        get_nodes = response.xpath('//div[@id="subject_list"]/ul/li/div[@class="pic"]/a')
        for node in get_nodes:
            url = node.xpath("@href").get()
            img_url = node.xpath('img/@src').get()
            yield Request(url=url, meta={"img_url": img_url}, callback=self.parse_book)
            
        next_url = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').get()
        if(next_url):
            yield Request(url=urljoin(response.url, next_url), callback=self.parse)
        
    def parse_book(self, response):

        BookItem = BookspiderItem()
        BookItem['name']     = response.xpath('//span[@property="v:itemreviewed"]/text()').get("").strip()
        BookItem['author']   = response.xpath('//span[contains(text(), "作者")]/following-sibling::a[1]/text()').get("").split()[-1]
        BookItem['publish']  = response.xpath('//span[contains(text(), "出版社")]/following-sibling::text()').get("").strip()
        
        page_num = response.xpath('//span[contains(text(), "页数")]/following-sibling::text()').get("").strip()
        BookItem['page_num'] = 0 if(page_num == '') else page_num

        BookItem['isbm']     = response.xpath('//span[contains(text(), "ISBN")]/following-sibling::text()').get("").strip()
        BookItem['binding']  = response.xpath('//span[contains(text(), "装帧")]/following-sibling::text()').get("").strip()
        BookItem['publish_date'] = response.xpath('//span[contains(text(), "出版年")]/following-sibling::text()').get("").strip()

        price    = response.xpath('//span[contains(text(), "定价")]/following-sibling::text()').get("").strip()
        BookItem['price']    = '' if(len(price) == 0) else re.findall(r'\d+\.?\d*', price)[0]

        BookItem['rate'] = response.xpath('//div[contains(@class, "rating_self ")]/strong/text()').get("").strip()

        BookItem['img_url'] = [response.meta.get('img_url')]

#        item_loader = BookItemLoader(item=BookspiderItem(), response=response)
#        item_loader.add_xpath("name", '//span[@property="v:itemreviewed"]/text()')
#        item_loader.add_xpath("author", '//span[contains(text(), "作者")]/following-sibling::a[1]/text()')
#        item_loader.add_xpath("publish", '//span[contains(text(), "出版社")]/following-sibling::text()')
#        item_loader.add_xpath("page_num", '//span[contains(text(), "页数")]/following-sibling::text()')
#        item_loader.add_xpath("isbm", '//span[contains(text(), "ISBN")]/following-sibling::text()')
#        item_loader.add_xpath("binding", '//span[contains(text(), "装帧")]/following-sibling::text()')
#        item_loader.add_xpath("publish_date", '//span[contains(text(), "出版年")]/following-sibling::text()')
#        item_loader.add_xpath("price", '//span[contains(text(), "定价")]/following-sibling::text()')
#        item_loader.add_xpath("rate", '//div[contains(@class, "rating_self ")]/strong/text()')
#        item_loader.add_value("img_url", [response.meta.get('img_url')])
#        BookItem = item_loader.load_item()
        
        yield BookItem
