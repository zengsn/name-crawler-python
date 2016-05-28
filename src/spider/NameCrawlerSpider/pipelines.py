# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from processData import *

class NamecrawlerspiderPipeline(object):

    def __init__(self):
        self.sentences = []
        startJVM(getDefaultJVMPath(),"-Djava.class.path=/Users/yangyunshen/name-crawler-python/src/spider/NameCrawlerSpider/hanlp-1.2.9.jar:/Users/yangyunshen/name-crawler-python/src/spider/NameCrawlerSpider","-Xms1g", "-Xmx1g")

    def process_item(self, item, spider):
        #如果article不存在数据则丢弃
        vaild = True
        if len(item['article']) == 0:
            vaild = False
            print '数据未通过'
            #raise DropItem("Missing article from %s" %item['url'])
        if vaild:
            for sentence in item['article']:
                self.sentences.append((sentence.encode('utf-8')))

            print '这是句子'
            for i in self.sentences: print i

            data = ProcessData(self.sentences)
            data_result = data.process_data()
            print '这是结果'
            print data_result

            #把title article内的数据编码并输出
            with open('/Users/yangyunshen/name-crawler-python/src/spider/item.json', 'a') as f:
                f.write(item['date'])
                f.write('\n')
                f.write('title:')
                for text in item['title']:
                    f.write(text.encode('utf-8'))
                f.write('\n')
                for key, values in data_result.items():
                    f.write(key + ':')
                    for value in values:
                        f.write(value + ',')
                    f.write( '\n')

            #     f.write('article:')
            #     for article in item['article']:
            #         f.write(article.encode('utf-8') + '\n')
            #     f.write(item['url'])
            #     f.write('\n')
            # f.close()

            print ' %s 数据通过管道 ' %item['date']
        return item

    def close_spider(self, spider):
        shutdownJVM()