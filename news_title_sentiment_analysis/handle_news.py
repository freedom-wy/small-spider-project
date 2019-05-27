import time
import requests
import json
from news_title_sentiment_analysis.setting import ak,sk


class HandleNewsTitle(object):
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type":"application/json",
        }
        self.ak = ak
        self.sk = sk
        self.baidu_token = ''
        self.baidu_analysis_api = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"
        self.news_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Content-Type": "application/json; charset=utf-8",
        }

    def handle_baidu_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(self.ak,self.sk)
        response = requests.get(url=host,headers=self.header)
        self.baidu_token = json.loads(response.text)['access_token']

    def handle_analysis(self,text=None):
        '''
        log_id	uint64	请求唯一标识码
        sentiment	int	表示情感极性分类结果，0:负向，1:中性，2:正向
        confidence	float	表示分类的置信度，取值范围[0,1]
        positive_prob	float	表示属于积极类别的概率 ，取值范围[0,1]
        negative_prob	float	表示属于消极类别的概率，取值范围[0,1]
        '''
        post_url = self.baidu_analysis_api+'?access_token='+self.baidu_token
        data = {
            "text": text
        }
        response = requests.post(url=post_url,headers=self.header,data=json.dumps(data))
        response.encoding = 'gbk'
        print(response.text)

    def handle_news_list(self):
        start_time_input = input("请输入起始日期(19900101):")
        end_time_input = input("请输入结束日期(20190527):")
        start_time = int(time.mktime(time.strptime(start_time_input,"%Y%m%d")))*1000
        end_time = int(time.mktime(time.strptime(end_time_input,"%Y%m%d")))*1000
        url4 = "http://192.168.67.70:32001/server/api/query/list"
        data = {"taskId": 25,
                "channelList": ["news", "media", "weibo", "weixin", "tieba", "bbs", "blog", "video", "wenda", "app"],
                "keyWords": "万科,华夏幸福地产,东原地产,绿地集团,中海地产,万达集团,绿城集团,恒大地产,华润置地", "relatedWords": "",
                "startPubTime": start_time,
                "endPubTime": end_time,
                "from": 1, "size": 100, "minSentiment": "0",
                "maxSentiment": "1.0", "type": "title", "method": "post"}
        data_str = json.dumps(data, ensure_ascii=False)
        response = requests.post(url=url4, headers=self.news_header, data=data_str.encode())
        return json.loads(response.text)['data']

    def handle_post_analysis_value(self,news):
        post_url = "http://192.168.67.70:32001/server/api/label/addOrUpdate"
        data = {
            "title": news['title'],
            "labelSentiment": "common",
            "systemSentimentValue": news['sysSentiment'],
            "sentimentWords": "",
            "pubTime": news['pubTime'],
            "channel": "news",
            "docId": news['docId'],
            "taskId": 25,
            "titleSimHash": news['fields']['titleSimHash'][0],
            "sysAbstract": news['sysAbstract'],
            "method": "post"
        }
        data_str = json.dumps(data, ensure_ascii=False)
        print(data_str)
        # response = requests.post(url=post_url,headers=self.header,data=data.encode())


def main():
    test = HandleNewsTitle()
    test.handle_baidu_token()
    news_list = test.handle_news_list()
    for news in news_list:
        test.handle_analysis(news['title'])
        time.sleep(1/4)


if __name__ == '__main__':
    main()
