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
                'date': [],
                'url' : [],
                'from': [],
            }
            #添加提取规则
            self.name_compiled_rule = re.compile(r'.*?(?=/nr)')
            self.address_compiled_rule = re.compile(r'.*?(?=/ns)')



    def process_data(self):
        try:
            #java.lang.System.out.println("Hello World")
            # 名字识别接口
            StandradTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
        except:
            traceback.print_exc()
        else:
            for sentence in self.cases:
                for case in StandradTokenizer.segment(sentence):
                    hasName = self.name_compiled_rule.match(str(case))
                    hasAddress = self.address_compiled_rule.match(str(case))
                    if hasName:
                        #如果名字的数据不重复,添加进结果
                        if hasName.group().strip() not in self.exist:
                            self.exist.add(hasName.group().strip())
                            self.result['name'].append(hasName.group().strip())
                    if hasAddress:
                        #如果地址的数据不重复,添加进结果
                        if hasAddress.group().strip() not in self.exist:
                            self.exist.add(hasAddress.group().strip())
                            self.result['address'].append(hasAddress.group().strip())
            return self.result

