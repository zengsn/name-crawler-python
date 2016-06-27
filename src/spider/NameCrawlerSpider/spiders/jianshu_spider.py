# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings

from NameCrawlerSpider.items import NamecrawlerspiderItem

logger = logging.getLogger("jianshu_spider")

class NewsSpider(CrawlSpider):
    name = "jianshu"

    allowed_domains = ['www.jianshu.com', ]

    website_possible_httpstatus_list = [403, 404]
    handle_httpstatus_list = [403]

    #启动时进行爬取的url列表.
    #后续的URL从初始的URL获取到得数据提取
    start_urls = ['http://www.jianshu.com']

    #需要跟进的链接表达式
    # allow_url = [r'href="/p.*"']

    #不要跟进的链接表达式
    # deny_url = settings['DENY_URL']

    rules = [
        # Rule(LinkExtractor(allow=allow_url, deny=deny_url), callback='parse_news_item', follow=True),

        #这行留着添加新网站时去掉注释并注释上一个Rule方便在运行时观察测试
        Rule(LinkExtractor(allow=(r'/p.*')), callback='parse_jianshu_item', follow=True),
        Rule(LinkExtractor(allow=(r'/users.*')), callback='parse_users', follow=True),
        Rule(LinkExtractor(allow=(r'/collection.*')), callback='parse_collections', follow=True)
    ]



    #每个初始url完成下载后生成的Response对象将会作为唯一参数传递给该函数,此方法负责解析返回的数据
    #提取数据(生成Item)以及生成需要进一步处理的URL的Requst对象
    def parse_jianshu_item(self, response):


        # #对应不同网站的提取规则
        article_xpath = settings['ARTICLE_XPATH']

        date_re = settings['DATE_RE']

        if response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            logger.info("got page: ")
            item = NamecrawlerspiderItem()

            item['url'] = response.url
            item['data_from'] = response.url.split(".")[1]

            #提取时间
            item['date'] = re.findall(date_re.get(item['data_from']), response.body)[0]

            item['title'] = response.selector.xpath('//title/text()').extract()

            #有些网站的文章路径不同,提取后检查article是否无内容或者内容过少,使用另一种提取规则
            item['article'] = response.selector.xpath(article_xpath.get(item['data_from'])).extract()

            yield item


    #匹配到的用户链接服务器会重定向,如果有文章末尾一般是latest_articles,如果没有则为timeline
    #末尾可能有follows,timeline,latest_articles,top_articles
    def parse_users(self, response):
        pass


    #跟进专题
    def parse_collections(self, response):
        pass