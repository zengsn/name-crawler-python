# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from NameCrawlerSpider.items import NamecrawlerspiderItem

class TecentNewsSpider(CrawlSpider):
    name = "tecent"
    allowed_domains = ["news.qq.com"]
    #启动时进行爬取的url列表.
    #后续的URL从初始的URL获取到得数据提取
    start_urls = ["http://news.qq.com/"]

    rules = [
        Rule(LinkExtractor(allow=(r'http://news.*')), callback='parse_item')
    ]


    #每个初始url完成下载后生成的Response对象将会作为唯一参数传递给该函数,此方法负责解析返回的数据
    #提取数据(生成Item)以及生成需要进一步处理的URL的Requst对象
    def parse_item(self, response):
        item = NamecrawlerspiderItem()
        item['url'] = response.url
        item['date'] = response.url.split("/")[-2]
        item['title'] = response.selector.xpath('//title/text()').extract()

        item['article'] = response.selector.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract()


        return item
