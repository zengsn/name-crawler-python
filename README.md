# name-crawler-python
Chinese name crawler written by Python


# 安装运行环境

####安装Java&Jpype
  参考 [Python调用自然语言处理包HanLP](http://www.hankcs.com/nlp/python-calls-hanlp.html)

####安装scrapy
	pip install scray

OS X安装中出现问题可以参考[安装Scrapy](https://segmentfault.com/n/1330000003944169)

####下载HanLP

下载配置版&data:
<https://github.com/hankcs/HanLP/releases>

下载完毕后需要把jar文件跟properties 放在项目目录下的HanLP文件夹里面 并修改hanlp.properties文件的第一行

	root=usr/home/HanLP/
为data的父目录即可,比如data目录是`/Users/hankcs/Documents/data`,那么`root=/Users/hankcs/Documents/`

####安装mongodb
前往官方主页下载<http://www.mongodb.org/downloads>

项目使用mongodb的默认localhost和端口,如果需要修改相关参数设置,可以在settings中修改

# 运行项目
在项目Spider目录下,使用命令行输入

	scrapy crawl tecent
