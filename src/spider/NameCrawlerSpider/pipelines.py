# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class NamecrawlerspiderPipeline(object):
    def process_item(self, item, spider):
        #如果article不存在数据则丢弃
        vaild = True
        if not 'article' in item.keys():
            vaild = False
            #raise DropItem("Missing article from %s" %item['url'])
        if vaild:
            #把title article内的数据编码并输出
            with open('/Users/yangyunshen/name-crawler-python/src/spider/item.json', 'a') as f:
                f.write(item['date'])
                f.write('\n')
                f.write('title:')
                for text in item['title']:
                    f.write(text.encode('utf-8'))
                f.write('\n')

                f.write('article:')
                for text in item['article']:
                    f.writelines(text.encode('utf-8'))
                f.write('\n')
            f.close()

        print ' %s 数据通过管道 ' %item['date']
        return item
