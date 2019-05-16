# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64


class MafengwoProxyMiddleware(object):
    #设置代理策略
    def process_request(self, request, spider):
        # proxy，主机头和端口号
        request.meta['proxy'] = 'http://http-dyn.abuyun.com:9020'
        # 用户名:密码,当前代理必须要有费用
        # 你自己买的代理，用户名和密码肯定和我的不一样
        proxy_name_pass = 'HTK32673HL02BK2D:50125D2D38937C94'.encode('utf-8')
        encode_pass_name = base64.b64encode(proxy_name_pass)
        # 将代理信息设置到头部去
        # 注意！！！！！Basic后面有一个空格
        request.headers['Proxy-Authorization'] = 'Basic ' + encode_pass_name.decode()

    #通过response判断下载是否成功
    def process_response(self, request, response, spider):
        if 'mafengwo.net' in request.url:
            return response
        elif response is None:
            return request
        elif response.status == 302:
            return request
        elif response.status == 403:
            return request
        elif 'flashcookie.sw' in response.text:
            return request
        else:
            return response
