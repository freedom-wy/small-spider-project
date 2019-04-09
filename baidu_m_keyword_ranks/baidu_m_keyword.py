import urllib
import re
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from baidu_m_keyword_ziran.handle_mysql import mysql
from baidu_m_keyword_ziran.handle_mongo import mongo
import time


class Handle_baidu_m(object):
    def __init__(self):
        self.header = {
            "Host":"m.baidu.com",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
        }

    #处理标题中的特殊字符
    def handle_title(self,title):
        search = re.compile('"|“|”|{|}')
        search_list = search.findall(title)
        for value in search_list:
            return re.sub(search,urllib.parse.quote(value),title)
        else:
            return title

    #处理任务
    def handle_task(self,keyword):
        print(keyword)
        result = {}
        result_list = []
        result['keyword'] = keyword
        url_list = ["http://m.baidu.com/s?pn=0&word="+keyword,"http://m.baidu.com/s?pn=10&word="+keyword,"http://m.baidu.com/s?pn=20&word="+keyword]
        for url in url_list:
            response = requests.get(url=url,headers=self.header)
            baidu_html = etree.HTML(response.text)
            item_list = baidu_html.xpath("//div[@id='results']/div")
            for item in item_list:
                info = {}
                #获取标题
                title = item.xpath(".//span[contains(@class,'title')]//text()|.//header[@class='c-row']/a/h3[@class='c-title']//text()")
                if title:
                    info['title'] = self.handle_title(''.join(title)).replace("'","")
                    if '百度百科' in info['title']:
                        info['target_url'] = "https://wapbaike.baidu.com/item/"+keyword
                    if '其他人还在搜' in info['title']:
                        continue
                    if '相关词语' in info['title']:
                        continue
                    if '相关平台' in info['title']:
                        continue
                    if '相关品牌' in info['title']:
                        continue
                    if '相关网站' in info['title']:
                        continue
                    if keyword+' - 资讯' in info['title']:
                        info['target_url'] = 'http://m.baidu.com/sf/vsearch?pd=realtime&word='+keyword
                    if keyword+' - 视频' in info['title']:
                        info['target_url'] = 'http://m.baidu.com/sf/vsearch?pd=video&atn=index&tn=vsearch&word='+keyword
                    if keyword+' - 小视频' in info['title']:
                        info['target_url'] = 'http://m.baidu.com/sf/vsearch?pd=xsp&atn=index&tn=vsearch&word='+keyword
                    else:
                        target_url = eval(item.xpath("./@data-log")[0].encode('utf-8').decode())['mu']
                        if target_url:
                            info['target_url'] = target_url
                        else:
                            if '_企业信息' in info['title']:
                                info['target_url'] = item.xpath("//a[@class='c-blocka']/@data-url")[0]
                    result_list.append(info)
                else:
                    continue
        result['rank'] = result_list
        result['crawl_time'] = time.strftime("%Y-%m-%d", time.localtime())
        print(result)
        # mongo.insert_item_in_db('baidu_m_keyword_ziran',result)
        # mysql.handle_insert_db(result)

if __name__ == '__main__':
    baidu_m = Handle_baidu_m()
    # baidu_m.handle_task('盐城二手奥迪a1')
    #线程池
    t = ThreadPoolExecutor()
    thread_list = []
    #获取任务
    task = mysql.handle_task()
    for keyword in task:
        thread = t.submit(baidu_m.handle_task,keyword[0])
        thread_list.append(thread)
    t.shutdown()
    # print([thread.result() for thread in thread_list])
