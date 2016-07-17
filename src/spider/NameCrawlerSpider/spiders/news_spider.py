# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import os
from ..htmlArticle import HtmlArticle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from logging.handlers import RotatingFileHandler
from NameCrawlerSpider.items import NamecrawlerspiderItem

logger = logging.getLogger(__name__)


class NewsSpider(CrawlSpider):
    name = "news"

    # allowed_domains = settings['ALLOWED_DOMAINS']

    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]

    # 启动时进行爬取的url列表.
    # 后续的URL从初始的URL获取到得数据提取
    start_urls = settings['START_URLS']

    # 需要跟进的链接表达式
    allow_url = settings['ALLOW_URL']

    # 不要跟进的链接表达式
    deny_url = settings['DENY_URL']

    rules = [
        Rule(LinkExtractor(allow=allow_url, deny=deny_url), callback='parse_news_item', follow=True),

        # 这行留着添加新网站时去掉注释并注释上一个Rule方便在运行时观察测试
        # Rule(LinkExtractor(allow=(r'http://news.qq.com/a/\d+/.*?')), callback='parse_news_item', follow=True),
    ]

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')

    FILE = os.getcwd() + '/log/'

    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    # 输出spider运行的日志
    Rthandler = RotatingFileHandler(os.path.join(FILE, 'spider_log.txt'), maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logger.addHandler(Rthandler)

    # 每个初始url完成下载后生成的Response对象将会作为唯一参数传递给该函数,此方法负责解析返回的数据
    # 提取数据(生成Item)以及生成需要进一步处理的URL的Requst对象
    def parse_news_item(self, response):

        date_re_article = settings['DATE_RE_ARTICLE']
        date_re = settings['DATE_RE']
        has_time = []
        time_use_default = False

        if response.status == 403:
            req = response.request
            req.meta["change_proxy"] = True
            logging.warning('403 from {}, now change proxy'.format(response.url))
            yield req
        else:
            logger.info("got page: ")
            item = NamecrawlerspiderItem()

            item['url'] = response.url
            item['data_from'] = response.url.split(".")[1]

            # 检查当前站点是否有另一种规则提取时间
            if date_re_article.has_key(item['data_from']):
                has_time = re.findall(date_re_article.get(item['data_from']), response.url)
            elif date_re.has_key(item['data_from']):
                has_time = re.findall(date_re.get(item['data_from']), response.url)
            else:
                date = re.findall(date_re.get('default'), response.url)  # 没有的话使用默认
                if len(date) > 0:
                    item['date'] = date[0]
                    time_use_default = True

            if has_time:
                item['date'] = '-'.join(map(str, has_time[0]))
            else:
                if not time_use_default:
                    item['date'] = 'none'


            item['title'] = response.selector.xpath('//title/text()').extract()

            # 提取文章
            htmlarticle = HtmlArticle()
            item['article'] = htmlarticle.get_html_article(response.body)

            yield item
