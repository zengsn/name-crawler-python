# -*- coding: utf-8 -*-

import os
import subprocess
from scrapy.conf import settings


def setting(option):
    #cat vim
    terminal = '{} {}{}settings.py'.format(option, os.getcwd(), '/NameCrawlerSpider/')
    return terminal


def runspider(spidername):
    terminal = 'scrapy crawl {spidername}'.format(spidername=spidername)
    return terminal


def mongoexport(out, type='json', database=settings['MONGODB_DB'],
                collection=settings['MONGODB_COLLECTION'], fields=None):
    if type.lower() not in ('csv', 'json'):
        print 'type error! it must be csv or json'
        return
    # 如果输入格式为csv并且给了fileds项
    elif type.lower() == 'csv':
        if not fields:
            print 'Export in CSV Format needs fields parameter!'
            return
        terminal = "mongoexport --db {} --collection {} --type=csv  \
                   --fields {} --out {}".format(database, collection, fields, out)
        return terminal
    else:
        # 默认输出json格式
        terminal = 'mongoexport --db {} --collection {} --out {}'.format(database, collection, out)
        return terminal


if __name__ == '__main__':
    option = raw_input('setting or runspider or ,mongoexport: ')
    while (option != 'q'):
        if option == 'setting':
            setting_option = raw_input('cat or vim to show & edit spider settings, q to quit(): \n>>>')
            if setting_option.lower() in ('vim', 'cat'):
                subprocess.call(setting(setting_option), shell=True)
            elif setting_option.lower() == 'q':
                option = ''
                continue

        elif option == 'runspider':
            print "now show the spider list"
            subprocess.call('scrapy list', shell=True)
            spidername = raw_input('please input spidername in list: \n>>>')
            subprocess.call(runspider(spidername), shell=True)

        elif option == 'mongoexport':
            type = raw_input('json or csv?: \n>>>')
            if type.lower() == 'csv':
                field = raw_input('please input fileds. example "name,records,search_count": \n>>>')
            if not field:
                print 'no fileds!'
                option = ''
                continue
            filename = raw_input('please input finename or dir/filename: \n>>>')
            subprocess.call(mongoexport(out=filename, type=type, fields=field), shell=True)
        option = raw_input('\n what do you want do next? ("q" to quit) \n>>>')

    print 'bye'

