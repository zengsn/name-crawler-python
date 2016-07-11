# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

import os
import logging
from scrapy.exceptions import DropItem
from datetime import datetime, timedelta
from scrapy.conf import settings
from processData import *


class FilterSamePage(object):
    """
    在爬取过程中发现会爬取到内容一样的页面,区别URL相似&下方评论不同.造成重复爬取.
    需要处理防止多次解析一样的内容.
    """

    # 记录来自简书的页面
    _jianshu_page = set()
    # 运行一段时间后set内容会比较大,而且爬过的url不会重复被抓.需要清理
    _clean_set_time = datetime.now()

    def process_item(self, item, spider):
        if item['data_from'] == 'jianshu':
            page_number = item['url'].split('/')[4]
            if page_number not in FilterSamePage._jianshu_page:
                # page_number不同表示爬取了新的页面,这时候检查下爬虫是否运行时间了一定的时间,清理集合
                if datetime.now() > FilterSamePage._clean_set_time + timedelta(minutes=20):
                    FilterSamePage._jianshu_page.clear()
                FilterSamePage._jianshu_page.add(page_number)

                return item
            else:
                raise DropItem('the page already has crawled')
        else:
            return item


class NamecrawlerspiderPipeline(object):
    def __init__(self):
        self.data_result = []
        jvm_path = '-Djava.class.path=' + os.getcwd() + '/HanLP/hanlp-1.2.9.jar:' + os.getcwd() + '/HanLP'
        startJVM(getDefaultJVMPath(), jvm_path, "-Xms1g", "-Xmx1g")
        # 建立一个connection
        client = pymongo.MongoClient(settings['MONGODB_URI'])
        # 获取数据库对象
        db = client[settings['MONGODB_DB']]
        # 获取数据库的collection(类似别的数据库中的'表')
        self.collection = db[settings['MONGODB_COLLECTION']]

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myspider.log',
                            filemode='w')

    def process_item(self, item, spider):
        sentences = []
        # 如果article不存在数据则丢弃
        has_article = True
        if len(item['article']) == 0:
            has_article = False
            # print '数据未通过'
            raise DropItem(u'Missing article from {0:s}'.format(item['url']))
        if has_article:
            for sentence in item['article']:
                sentences.append(sentence.encode('utf-8'))

            # print '这是句子'
            # for i in sentences:
            #     print i

            data = ProcessData(sentences)
            # 返回的是一个列表,里面每一项都是字典
            self.data_result = data.process_data()

            # 添加字典其余项并写进数据库
            for result in self.data_result:
                result['records']['date'] = item['date']
                result['records']['url'] = item['url']
                result['records']['from'] = item['data_from']
                self.collection.insert(result)
            print ' %s 数据通过管道 ' % item['date']
            message = "Item wrote to MongoDB database {0} {1}".format(settings['MONGODB_DB'],
                                                                      settings['MONGODB_COLLECTION'])
            logging.debug(message)

        return item

    def close_spider(self, spider):
        shutdownJVM()
