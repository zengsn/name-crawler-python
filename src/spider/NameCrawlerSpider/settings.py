# -*- coding: utf-8 -*-

# Scrapy settings for NameCrawlerSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'NameCrawlerSpider'

SPIDER_MODULES = ['NameCrawlerSpider.spiders']
NEWSPIDER_MODULE = 'NameCrawlerSpider.spiders'



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'NameCrawlerSpider (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'NameCrawlerSpider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 351,
    # put this middleware after RetryMiddleware
    # 'NameCrawlerSpider.HttpProxyMiddleware.HttpProxyMiddleware': 543,
}
DOWNLOAD_TIMEOUT = 10

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'NameCrawlerSpider.pipelines.NamecrawlerspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

#mongodb的设置
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DB = 'SpiderData'
MONGODB_COLLECTION = 'data'


#spider设置

# ALLOWED_DOMAINS = ["news.qq.com", "news.sina.com.cn", 'www.chinanews.com',
#                   'news.sohu.com', 'news.ifeng.com', 'www.cankaoxiaoxi.com',
#                    'news.xinhuanet.com',
#                   ]

START_URLS = ["http://news.qq.com/", "http://news.sina.com.cn/", "http://www.chinanews.com",
              "http://news.sohu.com", 'http://news.ifeng.com', 'http://www.cankaoxiaoxi.com',
              "http://www.xinhuanet.com", "http://news.cctv.com",
              ]

#用正则表达式设置跟进哪些从页面中提取的链接
ALLOW_URL = [r'http://news.qq.*', r'http://news.sina.*', r'http://www.chinanews.*',
             r'http://news.sohu.*', r'http://news.ifeng.*', 'http://www.cankaoxiaoxi.*',
             r'http://news.xinhuanet.*', r'http://news.cctv.*']

#用正则表达式设置不跟进哪些从页面中提取的链接
DENY_URL = [r'http://news.qq.com/original.*', r'http://.*shipin.*', r'http://.*video.*']

#使用xpath规则来提取,格式为'爬取站点':xpath表达式
#爬取站点需要一般为www.example.com中的'example'
ARTICLE_XPATH = {
            'qq':  "//div[@id='Cnt-Main-Article-QQ']/p/text()",
            'sina': '//div[@id="artibody"]/p/text()',
            'sina2': '//div[@id="artibody"]/p/span/text()',
            'chinanews' : "//div[@class='left_zw']/p/text()",
            'sohu': "//div[@itemprop='articleBody']/p/text()",
            'sohu2': "//div[@id='contentText']/p/text()",
            'ifeng': "//div[@id='main_content']/p/text()",
            'ifeng2': "//div[@id='artical_real']/p/text()",
            'cankaoxiaoxi': "//div[@id='ctrlfscont']/p/text()",
            'xinhuanet': "//div[@class='article']/p/text()",
            'cctv': '//div[@class="cnt_bd"]/p/text()',

        }

#有些网站里面的一部分文章需要另一种规则
#目前只支持2种规则设置
OTHER_XPATH_ALLOW = ['sina']

#从news类页面url中提取时间的表达式
#需要额外添加时格式为'爬取站点':re表达式
DATE_RE = {
    'default': r'/([\d-]+)/',
    'xinhuanet': r'/([\d-]+)/(\d+)/',
    'cctv': r'/([\d-]+)/(\d+)/(\d+)/',
}