# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

def handle_author(value):
    return value.split()[-1]

def handle_page_num(value):
    return 0 if(value == '') else value

def handle_price(value):
    return value

def handle_space(value):
    return value if(value == '') else value.strip()

def return_value(value):
    return value

class BookItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def add_xpath(self, field_name, xpath, *processors, **kw):
        values = self._get_xpathvalues(xpath, **kw)
        if values:
            self.add_value(field_name, values, *processors, **kw)
        else:
            self.add_value(field_name, '', *processors, **kw)

class BookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field(
#        input_processor = MapCompose(handle_author)
    )
    publish = scrapy.Field()
    page_num = scrapy.Field(
#        input_processor = MapCompose(handle_space, handle_page_num)
    )
    isbm = scrapy.Field()
    binding = scrapy.Field(
#        input_processor = MapCompose(handle_space)
    )
    publish_date = scrapy.Field(
#        input_processor = MapCompose(handle_space)
    )
    price = scrapy.Field(
#        input_processor = MapCompose(handle_space, handle_price)
    )
    rate = scrapy.Field()
    img_url = scrapy.Field(
#        output_processor = MapCompose(return_value)
    )
    image_path = scrapy.Field()
