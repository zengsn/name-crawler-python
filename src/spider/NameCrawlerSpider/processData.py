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
            self.address_extend_compiled_rule = re.compile(ur'(市|县)/n')

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
                # 提取到地址时临时临时存入.处理完毕后弹出到address
                address_sub = []
                # 记录是不是连续匹配到多个地址 把(多个)地址拼接
                address_count = 0
                address_str = ''
                # 检查是否匹配到了名字跟地址
                # 先匹配地址,再匹配人名
                has_match_address = False
                for case in StandradTokenizer.segment(sentence):
                    hasName = self.name_compiled_rule.match(str(case))
                    hasAddress = self.address_compiled_rule.match(str(case))
                    hasAddressExtend = self.address_extend_compiled_rule.match(str(case))
                    if hasName:
                        address_count = 0
                        # 匹配到名字前先匹配到地址
                        if len(address) > 0:
                            # 如果名字的数据不重复,添加进结果
                            if hasName.group().strip() not in self.exist:
                                self.exist.add(hasName.group().strip())
                                self.result_list.append(
                                    dict(name=hasName.group().strip(),
                                         records=dict(address=address.pop(-1))))
                            # 重置
                            address = []
                            address_str = ''
                    elif hasAddress:
                        address_count += 1
                        address_sub.append(hasAddress.group().strip())
                    elif hasAddressExtend:
                        # 处理这个需要前面匹配到地址
                        if address_count > 0:
                            address_count += 1
                            address_sub.append(hasAddressExtend.groups()[0].strip())
                    else:
                        if address_count > 0:
                            address_str = ''.join(map(str, address_sub))
                            address.append(address_str)
                            address_sub = []
                            # 如果地址的数据不重复,添加进结果
                            if address_str not in self.exist:
                                self.exist.add(address_str)
                        address_count = 0

            return self.result_list
