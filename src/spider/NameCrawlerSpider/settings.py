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

# 设置该属性可以使爬虫暂停/恢复(但是有时候会失效)
JOBDIR='crawls/spider'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'NameCrawlerSpider (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# 下载延时
# DOWNLOAD_DELAY = 5

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'NameCrawlerSpider.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 351,
    'NameCrawlerSpider.random_user_agent.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 取消掉下个注释可以启动代理功能
    # 'NameCrawlerSpider.HttpProxyMiddleware.HttpProxyMiddleware': 543,
}

DOWNLOAD_TIMEOUT = 10

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {

    # 'NameCrawlerSpider.pipelines.FilterSamePage': 299,
    'NameCrawlerSpider.pipelines.NamecrawlerspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'


USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
]

# mongodb的设置
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DB = 'SpiderData'
MONGODB_COLLECTION = 'data'
# 姓，拆开的名字，没拆开的名字分别存入不同数据库计数
MONGODB_FIRST_COL = 'FirstName'
MONGODB_LAST_COL = 'LastName'
MONGODB_FULL_LAST_COL = 'LastName2'

# spider设置

ALLOWED_DOMAINS = ["news.qq.com", "news.sina.com.cn",
                   'news.sohu.com', 'news.ifeng.com', 'news.xinhuanet.com', 'news.cctv.com'
                   ]

START_URLS = ["http://news.qq.com/", "http://news.sina.com.cn/",
              "http://news.sohu.com", 'http://news.ifeng.com', "http://www.xinhuanet.com", "http://news.cctv.com",
              ]

# 用正则表达式设置跟进哪些从页面中提取的链接
ALLOW_URL = [r'http://news.qq.com/a/\d+/.*?', r'http://news.sina.com.cn/\w/\w{2}/[\d-]+/.*?',
             r'http://news.sohu.com/\d{8}/.*?',
             r'http://news.ifeng.com/a/\d+/.*?', r'http://news.xinhuanet.com/\w+/[\d-]+/\d{2}/.*?',
             r'http://news.cctv.com/\d+/\d{2}/\d{2}/.*?']

# 用正则表达式设置不跟进哪些从页面中提取的链接
DENY_URL = [r'http://news.qq.com/original.*', r'http://.*shipin.*', r'http://.*video.*', r'.*english.*']

# 自定义从页面中提取时间. 格式与DATE_RE相同
# 会优先检测这里
DATE_RE_ARTICLE = {

}

# 从news类页面url中提取时间的表达式
# 需要额外添加时格式为'爬取站点':re表达式
DATE_RE = {
    'default': r'/([\d-]+)/',
    'xinhuanet': r'/([\d-]+)/(\d+)/',
    'cctv': r'/([\d-]+)/(\d+)/(\d+)/',
    'jianshu': r'([\d.]+)\s[\d:]+',
}

# 提取名字的过滤
PROCESS_RULE = {
    'name': r'(地|—|一|各|在|以|则|的|说|裔|岛|有|人|系|里|将|才|称|最|某|和|才|是|姓|要|外|也|都|吧|以|从|又|对|并|一位|一片|那年|坦克|书记|先生|女士|大妈|主任|主席|经理|总理|老板|同学|警官|全国|小编|师傅|小姐|男士|学院|披萨|海空|马航|马里|军方|空军|忠诚|陆军|总|华盛顿)',
    'address': r'(不|王子|院|地|的|局|街道|车|阿拉伯|芝加哥|星|洲|小区|天台|科隆|苏联|捷克|尼斯|伊斯兰|华盛顿|拉斯|程序|巴黎|纽约|伊拉克|以色列|多国|学院|洋|餐厅|非|瑞典|伊朗|医生|柬埔寨|马里|缅甸|希腊|德州|洋|队|防|市场|学院|西方|叙利亚|伊朗|澳大利亚|越南|波斯|乌克兰|朝鲜|开罗|韩国|白宫|美|日|菲律宾|法|土耳其|欧|意|俄|耶路撒冷|巴勒斯坦|德国|英国|比利时|阿富汗|巴基斯坦|莫斯科|泰国|苏格拉|埃及|加拿大|墨西哥|印度|南海|个|医院|夏天|政府)'
}
