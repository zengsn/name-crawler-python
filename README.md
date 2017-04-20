# name-crawler-python
Chinese name crawler written by Python


# 安装运行环境

##安装Java&Jpype
  参考 [Python调用自然语言处理包HanLP](http://www.hankcs.com/nlp/python-calls-hanlp.html)
  装好java后如果找不到java安装目录可以使用`update-alternatives --config java`来查看。
  配置bash里的JAVA_HOME环境变量再装Jpype。
  如果安装过程中报错jni.h not found则把java/include中的jni.h和jni_md.h复制一份到jpype/src/native/common/include

##下载HanLP

下载配置版&data:
<https://github.com/hankcs/HanLP/releases>

下载完毕后需要把jar文件跟properties 放在项目目录下的HanLP文件夹里面 并修改hanlp.properties文件的第一行

	root=usr/home/HanLP/
为data的父目录即可,比如data目录是`/Users/hankcs/Documents/data`,那么`root=/Users/hankcs/Documents/`


##安装依赖
    ``pip install -r require.txt``

OS X安装中出现问题可以参考[安装Scrapy](https://segmentfault.com/n/1330000003944169)

##安装flask(可选)
	pip install falsk

##安装mongodb
前往官方主页下载<http://www.mongodb.org/downloads>

项目使用mongodb的默认localhost和端口,如果需要修改相关参数设置,可以在settings中修改

# 运行项目
在项目Spider目录下,使用命令行输入,然后可以在相关提示下操作

	python main.py

同时项目自带了一个简单的restful api(需安装flask),命令行中在项目目录下

	python app.py

1. http://127.0.0.1:5000/count 会返回数据库的数据.
2. http://127.0.0.1:5000/api/v1.0/peoples/数字a/数字b 会返回数据库中第a~b条之间的所有数据
3. http://127.0.0.1:5000/api/v1.0/people/名字  会在数据库中查到该名字.成功则返回数据,失败会返回400
4. http://127.0.0.1:5000/api/v1.0/people/query  此接口需要用post方法.传递一个包含'name'字段的json. 若名字存在会返回{'name.exit': True}.名字不存在则会用程序识别是否为人名.是则加进数据库.

#数据演示

[NameCrawler Spider](http://name.chata.cn/name.chata.cn)