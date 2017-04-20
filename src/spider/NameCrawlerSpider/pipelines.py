# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

import logging
from logging.handlers import RotatingFileHandler
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from processData import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')


logger = logging.getLogger(__name__)


def getfile():
    allfiles = os.listdir(os.getcwd() + '/HanLP')
    r = re.compile(r'hanlp[-\d.]+jar')
    for f in allfiles:
        has_file = r.match(f)
        if has_file:
            return has_file.group()
    return None

# 检查是记录否唯一，不是插入，是则更新字段 插入拆开人名的时候使用
def ensure_one_and_update(collection, record, name):
    if not collection.find_one({record:name}):
        collection.insert({record:name, 'count':1})
    else:
        collection.update_one({record:name}, {'$inc':{'count':1}})
    return

def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value

class NamecrawlerspiderPipeline(object):
    def __init__(self):
        self.data_result = []
        # 获取Hanlp目录下文件与配置
        filename = getfile()
        if not isinstance(filename, str):
            logging.warning('the Hanlp file is not exist')
        jvm_path = '-Djava.class.path=' + os.getcwd() + '/HanLP/' + filename + ':' + os.getcwd() + '/HanLP'
        startJVM(getDefaultJVMPath(), jvm_path, "-Xms1g", "-Xmx1g")
        # 建立一个connection
        client = pymongo.MongoClient(settings['MONGODB_URI'])
        # 获取数据库对象
        db = client[settings['MONGODB_DB']]
        # 获取数据库的collection(类似别的数据库中的'表')
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.first_col = db[settings['MONGODB_FIRST_COL']]
        self.last_col = db[settings['MONGODB_LAST_COL']]
        self.full_last_col = db[settings['MONGODB_FULL_LAST_COL']]

        self.collection.ensure_index('name', unique=True, sparse=True)
        self.first_col.ensure_index('firstname', unique=True, sparse=True)
        self.last_col.ensure_index('lastname', unique=True, sparse=True)
        self.full_last_col.ensure_index('lastname2', unique=True, sparse=True)

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S')

        FILE = os.getcwd() + '/log/'

        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        # 将warning以上内容输出,方便用户查看什么网页内容抓取错误
        Rthandler = RotatingFileHandler(os.path.join(FILE, 'pipeline_log.txt'), maxBytes=10 * 1024 * 1024,
                                        backupCount=5)
        Rthandler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        Rthandler.setFormatter(formatter)
        logger.addHandler(Rthandler)

    def process_item(self, item, spider):
        sentences = []
        # 如果article以及data不存在则丢弃,并输出到日志文件方便用户检查
        if len(item['article']) == 0:
            raise DropItem(u'Missing article from {0:s}'.format(item['url']))
        elif len(item['date']) <= 6:
            logger.warning(u'wrong date from {0:s}'.format(item['url']))
            raise DropItem(u'wrong date from {0:s}'.format(item['url']))
        else:
            for article in item['article']:
                if isinstance(article, unicode) and len(article) > 200:
                    paragraph = article.split(u'\u3002')
                    for p in paragraph:
                        sentences.append(p)
                else:
                    sentences.append(article.encode('utf-8'))

            data = ProcessData(sentences)
            # 返回的是一个列表,里面每一项都是字典
            self.data_result = data.process_data()
            # 添加字典其余项并写进数据库
            try:
                for result in self.data_result:
                    result['records']['date'] = item['date']
                    result['records']['url'] = item['url']
                    result['records']['from'] = item['data_from']
                    result['name'] = to_unicode(result['name'])
                    # 检查数据库是否有这个人,如果没有就直接插入数据.
                    people = self.collection.find_one({'name':result['name']})
                    if not people:
                        result['records'] = result['records'] if isinstance(result['records'], list) else [result['records']]
                        result['records_count'] = 1
                        self.collection.insert(result)
                    else:
                        # 如果有的话 先把已存在的人数据取出来,更新records的值
                        newrecords = people['records'] if type(people['records']) == list else [people['records']]
                        newrecords.append(result['records'])
                        self.collection.update_one({'name': people['name']}, {'$inc':{'records_count':1}, '$set': {'records': newrecords}})
                    
                    if len(result['name']) == 2:
                        first_name = result['name'][0]
                        last_name = result['name'][1]
                        last_name2 = ''
                        full_last_name = result['name'][1]
                    elif len(result['name']) == 3:
                        first_name = result['name'][0]
                        last_name = result['name'][1]
                        last_name2 = result['name'][2]
                        full_last_name = result['name'][1:3]
                    elif len(result['name']) == 4:
                        first_name = result['name'][:2]
                        last_name = result['name'][2]
                        last_name = result['name'][3]
                        full_last_name = result['name'][2:4]

                    for count, col in enumerate([self.first_col, self.last_col, self.full_last_col]):
                        if count == 0:
                            ensure_one_and_update(col, 'FirstName', first_name)
                        if count == 2:
                            ensure_one_and_update(col, 'LastName2', full_last_name)
                        else:
                            if last_name:
                                ensure_one_and_update(col, 'LastName', last_name)
                            if last_name2:
                                ensure_one_and_update(col, 'LastName', last_name2)

                print ' %s 数据通过管道 ' % item['date']
                message = "Item wrote to MongoDB database {0} {1}".format(settings['MONGODB_DB'],
                                                                          settings['MONGODB_COLLECTION'])
                logging.debug(message)
            except Exception, e:
                logging.error('fail to write in database, the error is {}'.format(e))

        return item

    def close_spider(self, spider):
        shutdownJVM()



