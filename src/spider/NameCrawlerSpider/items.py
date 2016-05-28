# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NamecrawlerspiderItem(scrapy.Item):
    #item是保存爬取到得数据的容器
    #爬取的数据为文章,日期,标题
    #爬取到得文章应该在后续步骤中进一步处理
    title = scrapy.Field()
    article = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()

