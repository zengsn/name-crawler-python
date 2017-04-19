# -*- coding: utf-8 -*-

import sys
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf8')

CLIENT = MongoClient()
DB = CLIENT['SpiderData']
DATE_COL = DB['data']
FIRST_COL = DB['FirstName']
LAST_COL = DB['LastName']
FULL_LAST_COL = DB['LastName2']

RECORD_LIST = ['FirstName', 'LastName', 'LastName2']

FIRST_COL.ensure_index('firstname', unique=True, sparse=True)
LAST_COL.ensure_index('lastname', unique=True, sparse=True)
FULL_LAST_COL.ensure_index('lastname2', unique=True, sparse=True)

def ensure_one_and_update(collection, record, name):
    if not collection.find_one({record:name}):
        collection.insert({record:name, 'count':1})
    else:
        collection.update_one({record:name}, {'$inc':{'count':1}})
    return

for data in DATE_COL.find():
    print (u'正在处理{}'.format(data['name']))
    # 把姓，名字单词，名字全词分别拆开
    if len(data['name']) == 2:
        first_name = data['name'][0]
        last_name = data['name'][1]
        last_name2 = ''
        full_last_name = data['name'][1]
    elif len(data['name']) == 3:
        first_name = data['name'][0]
        last_name = data['name'][1]
        last_name2 = data['name'][2]
        full_last_name = data['name'][1:3]
    elif len(data['name']) == 4:
        first_name = data['name'][:2]
        last_name = data['name'][2]
        last_name = data['name'][3]
        full_last_name = data['name'][2:4]
    print(u'已经取得{}，{}，{}，{}'.format(first_name, last_name, last_name2, full_last_name))

    # 更新records计算，新增一个字段来计数records数量
    newrecords = data['records'] if isinstance(data['records'], list) else [data['records']]
    DATE_COL.update_one({'name': data['name']},
                        {'$set':{'records_count': len(data['records']), 'records': newrecords}},
                        upsert=True)

    for count, col in enumerate([FIRST_COL, LAST_COL, FULL_LAST_COL]):
        if count == 0:
            ensure_one_and_update(col, 'FirstName', first_name)
        if count == 2:
            ensure_one_and_update(col, 'LastName2', full_last_name)
        else:
            if last_name:
                ensure_one_and_update(col, 'LastName', last_name)
            if last_name2:
                ensure_one_and_update(col, 'LastName', last_name2)
    print(u'处理完毕！')
