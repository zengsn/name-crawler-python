# -*- coding:utf-8 -*-
import re
import sys
import os
import traceback
from jpype import *


class ProcessData(object):
    def __doc__(self):
        """
        这个类是调用Halp语言包来对传入的数据进行处理取出名字和地址.
        """

    def __init__(self, sentence):
        #传进来的sentence应该为一个列表
        if type(sentence) == list:
            self.cases = sentence
            #用集合来去除重复数据
            self.exist = set()
            # 存放提取结果的字典
            self.result = {
                'name': [],
                'address': [],
            }
            #添加提取规则
            self.name_compiled_rule = re.compile(r'.*?(?=/nr)')
            self.address_compiled_rule = re.compile(r'.*?(?=/ns)')



    def process_data(self):
        try:
            # 初始化Hanlp
            #cwd = '-Djava.class.path=' + os.getcwd() +'/hanlp-1.2.9.jar:./'
            # startJVM(getDefaultJVMPath(), "-Djava.class.path=/Users/yangyunshen/name-crawler-python/src/spider/NameCrawlerSpider/hanlp-1.2.9.jar:/Users/yangyunshen/name-crawler-python/src/spider/NameCrawlerSpider", "-Xms1g", "-Xmx1g")
            #startJVM(getDefaultJVMPath(), cwd, "-Xms1g", "-Xmx1g")
            java.lang.System.out.println("Hello World")
            # 名字识别接口
            StandradTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
        except:
            traceback.print_exc()
        else:
            for sentence in self.cases:
                for case in StandradTokenizer.segment(sentence):
                    # print str(case)
                    hasName = self.name_compiled_rule.match(str(case))
                    hasAddress = self.address_compiled_rule.match(str(case))
                    if hasName:
                        # print hasName.group().strip()
                        if hasName.group().strip() not in self.exist:
                            self.exist.add(hasName.group().strip())
                            self.result['name'].append(hasName.group().strip())
                    if hasAddress:
                        # print hasAddress.group().strip()
                        if hasAddress.group().strip() not in self.exist:
                            self.exist.add(hasAddress.group().strip())
                            self.result['address'].append(hasAddress.group().strip())
            #shutdownJVM()
            return self.result


#测试输出
if __name__ == '__main__':

    testCases = [
        "签约仪式前，秦光荣、李纪恒、仇和等一同会见了参加签约的企业家。",
        "王国强、高峰、汪洋、张朝阳光着头、韩寒、小四",
        "张浩和胡健康复员回家了",
        "王总和小丽结婚了",
        "编剧邵钧林和稽道青说",
        "这里有关天培的有关事迹",
        "龚学平等领导,邓颖超生前",
        "武胜县新学乡政府大楼门前锣鼓喧天",
        "蓝翔给宁夏固原市彭阳县红河镇黑牛沟村捐赠了挖掘机",
    ]


    test = ProcessData(testCases)
    result = test.process_data()

    for key, values in result.items():
        print key + ':'
        for value in values:
            print value,
        print '\n'

    print os.getcwd()