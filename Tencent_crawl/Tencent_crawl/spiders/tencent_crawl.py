# -*- coding: utf-8 -*-
import scrapy
# LinkExtractor 负责提取响应里的链接
from scrapy.linkextractors import LinkExtractor
# CrawlSpider 和 Rule 负责发送提取请求
from scrapy.spiders import CrawlSpider, Rule
from Tencent_crawl.items import TencentCrawlItem, PositionItem


class TencentCrawlSpider(CrawlSpider):
    name = 'tencent_crawl'
    allowed_domains = ['hr.tencent.com']
    # start_urls里的请求，返回的响应只做链接的提取，不做解析，因为prase被用作CrawlSpider做内部逻辑了，不能重写parse
    start_urls = ["http://hr.tencent.com/position.php?&start=0"]

    # 提取链接（去重）， Rule发送请求， LinkExtractor是链接提取器， callback处理， follow跟进提取
    rules = (
        # callback中写parse的名字，不写self.prase
        # 处理职位列表页的链接请求
        Rule(LinkExtractor(allow=r"position\.php\?&start="), callback="parse_item", follow=True),

        # 处理职位详情页的链接请求
        Rule(LinkExtractor(allow=r"position_detail\.php\?id=\d+"), callback="parse_position", follow=False)
    )

    def parse_item(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentCrawlItem()

            item['position_name'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['position_link'] = "http://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract()[0]

            try:
                item['position_type'] = node.xpath("./td[2]/text()").extract()[0]
            except:
                item['position_type'] = "None"

            item['people_number'] = node.xpath("./td[3]/text()").extract()[0]
            item['work_location'] = node.xpath("./td[4]/text()").extract()[0]
            item['publish_times'] = node.xpath("./td[5]/text()").extract()[0]

            yield item
            # meta 参数做为Request的请求一起发送，并随着response一起传递到指定的回调函数
            # meta做为response的属性传递
            #yield scrapy.Request(item['position_link'], meta = {"position_item" : item}, callback = self.parse_position)

    def parse_position(self, response):

        #item = response.meta["position_item"]
        item = PositionItem()

        item["position_zhize"] = " ".join(response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())

        item["position_yaoqiu"] = " ".join(response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())

        yield item

