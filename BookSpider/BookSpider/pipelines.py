# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from twisted.enterprise import adbapi

class BookspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ImageStorePipeline(ImagesPipeline):

    default_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            self.default_headers['referer'] = image_url
            yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        item['image_path'] = image_path
        return item

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):


        dbpool = adbapi.ConnectionPool("MySQLdb", host=settings['MYSQL_HOST'], db = settings['MYSQL_DBNAME'], user = settings['MYSQL_USER'], passwd = settings['MYSQL_PASSWORD'], charset = 'utf8', cursorclass = MySQLdb.cursors.DictCursor, use_unicode = True)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error,item,spider)
    
    def do_insert(self, cursor, item):
        insert_sql = """
            insert into douban(name, author, publish, page_num, isbm, binding, publish_date, price, rate, img_url, image_path)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_sql, (item['name'], item['author'], item['publish'], item['page_num'], item['isbm'], item['binding'], item['publish_date'], item['price'], item['rate'], item['img_url'], item['image_path']))

    def handle_error(self, failure, item, spider):
        print(failure)