# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
from jpype import *

#初始化Hanlp
startJVM(getDefaultJVMPath(), "-Djava.class.path=./hanlp-1.2.9.jar:./", "-Xms1g", "-Xmx1g")
HanLP = JClass('com.hankcs.hanlp.HanLP')

#存放提取结果的字典
result = {
    'name':[],
    'address':[],
}

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

#名字识别接口
StandradTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')

#提取数据的匹配规则
name_rule = r'.*?(?=/nr)'
address_rule = r'.*?(?=/ns)'
name_compiled_rule = re.compile(name_rule)
address_compiled_rule = re.compile(address_rule)

for sentence in testCases:
    for case in StandradTokenizer.segment(sentence):
        # print str(case)
        hasName = name_compiled_rule.match(str(case))
        hasAddress = address_compiled_rule.match(str(case))
        if hasName:
            #print hasName.group().strip()
            result['name'].append(hasName.group().strip())
        if hasAddress:
            #print hasAddress.group().strip()
            result['address'].append(hasAddress.group().strip())

for key, values in result.items():
    print key + ':'
    for value in values:
        print value,
    print '\n'

