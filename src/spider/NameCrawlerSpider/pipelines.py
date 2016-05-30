# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.exceptions import DropItem
from processData import *


class NamecrawlerspiderPipeline(object):

    def __init__(self):
        self.data_result = []
        startJVM(getDefaultJVMPath(),"-Djava.class.path=/Users/yangyunshen/name-crawler-python/src/spider/NameCrawlerSpider/hanlp-1.2.9.jar:/Users/yangyunshen/name-crawler-python/src/spider/NameCrawlerSpider","-Xms1g", "-Xmx1g")
        #建立一个connection
        client = pymongo.MongoClient()
        #获取数据库对象
        db = client.SpiderData
        #获取数据库的collection(类似别的数据库中的'表')
        self.collection = db.data


    def process_item(self, item, spider):
        sentences = []
        #如果article不存在数据则丢弃
        has_article = True
        if len(item['article']) == 0:
            has_article = False
            print '数据未通过'
            #raise DropItem("Missing article from %s" %item['url'])
        if has_article:
            for sentence in item['article']:
                sentences.append((sentence.encode('utf-8')))

            # print '这是句子'
            # for i in self.sentences: print i
            #
            data = ProcessData(sentences)
            self.data_result = data.process_data()
            # print '这是结果'
            # print data_result
            self.data_result['date'].append(item['date'])

            #把title article内的数据编码并输出
            # with open('/Users/yangyunshen/name-crawler-python/src/spider/item.json', 'a') as f:
            #     for key, values in self.data_result.items():
            #         f.write(key + ':')
            #         for value in values:
            #             f.write(value + ',')
            #         f.write( '\n')

            #写进数据库
            self.collection.insert(self.data_result)

            print ' %s 数据通过管道 ' %item['date']
        return item

    def close_spider(self, spider):
        shutdownJVM()