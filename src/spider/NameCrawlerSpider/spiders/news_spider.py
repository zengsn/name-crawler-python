# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from ..htmlArticle import HtmlArticle
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

    # 启动时进行爬取的url列表.
    # 后续的URL从初始的URL获取到得数据提取
    start_urls = settings['START_URLS']

    # 需要跟进的链接表达式
    allow_url = settings['ALLOW_URL']

    # 不要跟进的链接表达式
    deny_url = settings['DENY_URL']

    rules = [
        # Rule(LinkExtractor(allow=allow_url, deny=deny_url), callback='parse_news_item', follow=True),

        # 这行留着添加新网站时去掉注释并注释上一个Rule方便在运行时观察测试
        Rule(LinkExtractor(allow=(r'http://news.qq.com/a/\d+/.*?')), callback='parse_news_item', follow=True),
    ]

    # 每个初始url完成下载后生成的Response对象将会作为唯一参数传递给该函数,此方法负责解析返回的数据
    # 提取数据(生成Item)以及生成需要进一步处理的URL的Requst对象
    def parse_news_item(self, response):

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

            # 检查当前站点是否有另一种规则提取时间
            if date_re.has_key(item['data_from']):
                has_time = re.findall(date_re.get(item['data_from']), response.url)
                if has_time:
                    item['date'] = '-'.join(map(str, has_time[0]))
                else:
                    item['date'] = 'none'
            else:
                item['date'] = re.findall(date_re.get('default'), response.url)  # 没有的话使用默认

            item['title'] = response.selector.xpath('//title/text()').extract()

            # 提取文章
            htmlarticle = HtmlArticle()
            item['article'] = htmlarticle.get_html_article(response.body)

            yield item
