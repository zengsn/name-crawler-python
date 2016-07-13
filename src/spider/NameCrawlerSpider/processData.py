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
        # 传进来的sentence应该为一个列表
        if type(sentence) == list:
            self.cases = sentence
            # 用集合来去除重复数据
            self.exist = set()
            # 存放所有结果的列表,每一项都是一个字典
            self.result_list = []

            # 预编译正则表达式,使用的时候程序就不用重复分析正则表达式
            self.name_compiled_rule = re.compile(r'.*?(?=/nr)')
            self.address_compiled_rule = re.compile(r'.*?(?=/ns)')

    def process_data(self):
        try:
            # java.lang.System.out.println("Hello World")
            # 名字识别接口
            StandradTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
        except:
            traceback.print_exc()
        else:
            for sentence in self.cases:
                # 存放提取地址结果的列表
                address = []
                # 检查是否匹配到了名字跟地址
                # 先匹配地址,再匹配人名
                has_match_address = False
                for case in StandradTokenizer.segment(sentence):
                    hasName = self.name_compiled_rule.match(str(case))
                    hasAddress = self.address_compiled_rule.match(str(case))
                    if hasName:
                        # 如果名字的数据不重复,添加进结果
                        if hasName.group().strip() not in self.exist:
                            self.exist.add(hasName.group().strip())
                            # 匹配到名字前先匹配到地址
                            if has_match_address:
                                has_match_address = False
                                self.result_list.append(
                                    dict(name=hasName.group().strip(),
                                         records=dict(address=address.pop(-1))))
                    if hasAddress:
                        # 如果地址的数据不重复,添加进结果
                        if hasAddress.group().strip() not in self.exist:
                            has_match_address = True
                            self.exist.add(hasAddress.group().strip())
                            address.append(hasAddress.group().strip())

            return self.result_list
