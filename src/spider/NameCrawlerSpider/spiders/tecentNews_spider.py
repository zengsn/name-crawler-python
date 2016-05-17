# -*- coding: utf-8 -*-
import scrapy

from NameCrawlerSpider.items import NamecrawlerspiderItem

class TecentNewsSpider(scrapy.spiders.Spider):
    name = "tecent"
    allowed_domains = ["news.qq.com"]

    #启动时进行爬取的url列表.
    #后续的URL从初始的URL获取到得数据提取
    start_urls = ["http://news.qq.com/a/20160517/030099.htm"]


    #每个初始url完成下载后生成的Response对象将会作为唯一参数传递给该函数,此方法负责解析返回的数据
    #提取数据(生成Item)以及生成需要进一步处理的URL的Requst对象
    def parse(self, response):
        item = NamecrawlerspiderItem()
        item['date'] = response.url.split("/")[-2]
        item['title'] = response.selector.xpath('//title').extract()
        item['article'] = response.selector.xpath("//div[@id='Cnt-Main-Article-QQ']/p").extract()

        #如果直接输出内容为uncoide字符无法阅读 临时处理一下
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            for title in item['title']:
                f.writelines(title)

            for article in item['article']:
                f.writelines(article)

            f.close()