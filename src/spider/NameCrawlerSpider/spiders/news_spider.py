# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings

from NameCrawlerSpider.items import NamecrawlerspiderItem

logger = logging.getLogger("NewsSpider")

class NewsSpider(CrawlSpider):
    name = "news"

    # allowed_domains = settings['ALLOWED_DOMAINS']

    website_possible_httpstatus_list = [403, 404]
    handle_httpstatus_list = [403]

    #启动时进行爬取的url列表.
    #后续的URL从初始的URL获取到得数据提取
    start_urls = settings['START_URLS']

    #需要跟进的链接表达式
    allow_url = settings['ALLOW_URL']

    #不要跟进的链接表达式
    deny_url = settings['DENY_URL']

    rules = [
        Rule(LinkExtractor(allow=allow_url, deny=deny_url), callback='parse_news_item', follow=True),

        #这行留着添加新网站时去掉注释并注释上一个Rule方便在运行时观察测试
        # Rule(LinkExtractor(allow=(r'http://news.cctv.*')), callback='parse_news_item', follow=True),
    ]


    #每个初始url完成下载后生成的Response对象将会作为唯一参数传递给该函数,此方法负责解析返回的数据
    #提取数据(生成Item)以及生成需要进一步处理的URL的Requst对象
    def parse_news_item(self, response):

        #对应不同网站的提取规则
        article_xpath = settings['ARTICLE_XPATH']

        date_re = settings['DATE_RE']

        #有的网站才需要另一个规则
        other_xpath_allow = ['sina']
        # other_xpath_allow = ['sina']

        if response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            logger.info("got page: ")
            item = NamecrawlerspiderItem()

            item['url'] = response.url
            item['data_from'] = response.url.split(".")[1]

            #检查当前站点是否有另一种规则提取时间
            if date_re.has_key(item['data_from']):
                has_time = re.findall(date_re.get(item['data_from']), response.url)
                if has_time:
                    item['date'] = '-'.join(map(str,has_time[0]))
                else:
                    item['date'] = 'none'
            else:
                item['date'] = re.findall(date_re.get('default'), response.url)  #没有的话使用默认

            item['title'] = response.selector.xpath('//title/text()').extract()

            #有些网站的文章路径不同,提取后检查article是否无内容或者内容过少,使用另一种提取规则
            item['article'] = response.selector.xpath(article_xpath.get(item['data_from'])).extract()
            if len(item['article']) == 0 or len(item['article'][-1]) <= 10:
                if item['data_from'] in other_xpath_allow:
                    item['article'] = response.selector.xpath(article_xpath.get(item['data_from'] + '2')).extract()

            yield item

