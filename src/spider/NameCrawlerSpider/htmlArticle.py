# -*- coding:utf-8 -*-
import re
import urllib2
from readability import Document


class HtmlArticle(object):

    def remove_html_tag(self, response):
        r = re.compile(r'<[^>]+>', re.S)
        response = r.sub('', response)
        return response.strip()

    def remove_empty_line(self, response):
        r = re.compile(r'&#13;', re.M | re.S)
        response = r.sub('', response)
        r = re.compile(r'^\s+', re.M | re.S)
        response = r.sub('', response)
        r = re.compile(r'\n+', re.M | re.S)
        response = r.sub('\n', response)
        return response

    def get_html_article(self, response):
        """
        先调用readability识别正文,再去除标签以及空行,接下来因为模块识别出的正文会混入导航内容,需进一步处理
        具体做法是以换行符分割识别到内容,判断字数.取出是文章的项
        """

        readable_article = Document(response).summary()
        readable_article = self.remove_html_tag(readable_article)
        readable_article = self.remove_empty_line(readable_article)

        article_split = readable_article.split('\n')

        # 记录识别到文章开始和结束的位置
        begin = 0
        end = 0

        begin_find = False
        end_find = False
        has_article = False

        for index in range(len(article_split)):

            # # 当有一段特别大的时候只拿那一段
            # if len(article_split[index]) > 500:
            #     begin, end = index, index
            #     break

            if not begin_find:
                # 一项长度大于40的话就认为是文章的开头
                if len(article_split[index]) > 60:
                    begin = index
                    begin_find = True
                    has_article = True

            elif not end_find:
                if len(article_split[-index - 1]) == 0:
                    continue
                elif article_split[-index - 1][-1] in u'\u3002\uff01':
                    if len(article_split[-index - 1]) > 60:
                        end = index
                        end_find = True
                        has_article = True

        empty_list=[]

        if not has_article:
            return empty_list
        elif begin == end:
            empty_list.append(article_split[begin])
            return empty_list
        else:
            return article_split[begin: len(article_split) - end]

if __name__ == '__main__':
    a = HtmlArticle()

    url = 'http://news.qq.com/a/20160711/012641.htm#p=1'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    req = urllib2.Request(url)
    req.add_header(key=USER_AGENT, val=USER_AGENT)
    response = urllib2.urlopen(req)

    dd = a.get_html_article(response.read())
    for i in dd:
        print i

    # if isinstance(dd, str):
    #     print dd
    # else:
    #     for i in dd:
    #         print i+'\n'
    # # print response.read()