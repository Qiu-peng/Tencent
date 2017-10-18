# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from Tencent_crawl.items import TencentCrawlItem, PositionItem


class TencentCrawlPipeline(object):
    def __init__(self):
        self.f = open("tencent.json", "w")

    def process_item(self, item, spider):
        # 通过isinstance()判断  如果item是TencentItem类型，就为True
        if isinstance(item, TencentCrawlItem):
            content = json.dumps(dict(item)) + ",\n"
            self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()


class PositionPipeline(object):

    def __init__(self):
        self.f = open("position.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, PositionItem):
            content = json.dumps(dict(item)) + ",\n"
            self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()
