# 懂球帝新闻爬虫
### 需求
抓取懂球帝新闻https://dongqiudi.com/news
### 项目结构
```text
dongqiudi
    dongqiudi_pic   图片目录
    spiders         爬虫解析文件
    items.py        项目字段定义文件
    middlewares.py  中间件,包含下载代理中间件
    pipelines.py    数据管道,包含mongo数据存储和图片下载
    settings.py     配置文件
    main.py         启动文件
```
### 说明
```text
在pipelines.py中定义mongodb的ip地址和端口号
在settings.py中定义是否开启中间件,下载延迟等选项
```


#### bug:dazhuang_python@sina.com
