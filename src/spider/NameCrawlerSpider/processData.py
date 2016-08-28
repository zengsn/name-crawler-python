# -*- coding:utf-8 -*-
import re
import os
import traceback
from jpype import *
from scrapy.conf import settings
from pipelines import getfile



FIRSTNAME = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何',
             '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏',
             '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史',
             '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅',
             '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁',
             '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝',
             '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林',
             '刁', '钟', '徐', '邱', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫',
             '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔',
             '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁', '荀', '羊', '於', '惠', '甄', '麴', '家', '封', '芮', '羿',
             '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫', '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓',
             '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫', '宁', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘',
             '景', '詹', '束', '龙', '叶', '幸', '司', '韶', '郜', '黎', '蓟', '薄', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索',
             '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阴', '欎', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡',
             '劳', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '舄', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕',
             '冀', '郏', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容',
             '向', '古', '易', '慎', '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广',
             '禄', '阙', '东', '殴', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾',
             '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '後', '荆',
             '红', '游', '竺', '权', '逯', '盖', '益', '桓', '公', '仉', '督', '晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦', '归', '海',
             '岳', '帅', '缑', '亢', '况', '后', '有', '琴', '商', '牟', '佘', '佴', '伯', '赏', '南', '宫', '墨', '哈', '谯', '笪', '年',
             '爱', '阳', '佟', '言', '福', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫', '尉迟', '公羊', '澹台',
             '公冶',
             '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '钟离', '宇文', '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空',
             '亓官', '司寇', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', '壤驷', '公良', '拓跋', '夹谷', '宰父', '谷梁', '段干', '百里', '东郭',
             '南门', '呼延', '梁丘', '左丘', '东门', '西门', '南宫', '第五']


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
            self.address_extend_compiled_rule = re.compile(r'(市|县)(?=/n)')
            self.name_filter_rule = re.compile(settings['PROCESS_RULE']['name'])
            self.address_filter_rule = re.compile(settings['PROCESS_RULE']['address'])

    def is_name(self, name):
        try:
            # 初始化Hanlp
            filename = getfile()
            jvm_path = '-Djava.class.path=' + os.getcwd() + '/HanLP/' + filename + ':' + os.getcwd() + '/HanLP'
            if not isJVMStarted():
                startJVM(getDefaultJVMPath(), jvm_path, "-Xms1g", "-Xmx1g")

            # java.lang.System.out.println("Hello World")
            # 名字识别接口
            StandradTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
        except:
            traceback.print_exc()
        else:
            # java.lang.System.out.println("Hello World")
            # print testcase
            # print StandradTokenizer.segment(name)[0]
            hasName = self.name_compiled_rule.match(str(StandradTokenizer.segment(name)[0]))
            # shutdownJVM()
            if hasName:
                nameFilter = self.name_filter_rule.search(hasName.group().strip())
                if nameFilter:
                    return False
                elif 3 < len(hasName.group().strip()) <= 9:
                    if hasName.group().strip()[:3] not in FIRSTNAME or \
                                    hasName.group().strip()[:3] == hasName.group().strip()[3:6]:
                        return False
                elif 9 < len(hasName.group().strip()) <= 12:
                    if hasName.group().strip()[:6] not in FIRSTNAME:
                        return False
                elif len(hasName.group().strip()) > 12 or len(hasName.group().strip()) < 3:
                    return False

                return True
            else:
                return False

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
                            nameFilter = self.name_filter_rule.search(hasName.group().strip())
                            if nameFilter:
                                address.pop(-1)
                                break
                            elif 3 < len(hasName.group().strip()) <= 9:
                                if hasName.group().strip()[:3] not in FIRSTNAME or \
                                                hasName.group().strip()[:3] == hasName.group().strip()[3:6]:
                                    address.pop(-1)
                                    break
                            elif 9 < len(hasName.group().strip()) <= 12:
                                if hasName.group().strip()[:6] not in FIRSTNAME:
                                    address.pop(-1)
                                    break
                            elif len(hasName.group().strip()) > 12 or len(hasName.group().strip()) < 3:
                                address.pop(-1)
                                break
                            if hasName.group().strip() not in self.exist:
                                self.exist.add(hasName.group().strip())
                                self.result_list.append(
                                    dict(name=hasName.group().strip(),
                                         records=dict(address=address.pop(-1))))
                            # 重置
                            address = []
                    elif hasAddress:
                        adressFilter = self.address_filter_rule.search(hasAddress.group().strip())
                        if adressFilter:
                            address_sub = []
                            address_count = 0
                            break
                        address_count += 1
                        address_sub.append(hasAddress.group().strip())
                    elif hasAddressExtend:
                        # 处理这个需要前面匹配到地址
                        if address_count > 0:
                            address_count += 1
                            address_sub.append(hasAddressExtend.group().strip())
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
