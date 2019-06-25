# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random

class ProxyMiddleware(object):
    def __init__(self):
        self.proxy_info = [
            {'proxy_url': 'ip4.hahado.cn:35410', 'proxy_user_pass': b'duoipbpvzyymn:tRf6NnfsBi7k0'},
            {'proxy_url': 'ip4.hahado.cn:35164', 'proxy_user_pass': b'duoipcnezxjlvkv:xXuXTPES9XPwp'},
            {'proxy_url': 'ip4.hahado.cn:35401', 'proxy_user_pass': b'duoipwpdlrfwc:888888'},
            {'proxy_url': 'ip4.hahado.cn:35404', 'proxy_user_pass': b'duoipcnxgfzfsyp:TjgLhDqqEj0Pe'},
            {'proxy_url': 'ip4.hahado.cn:35413', 'proxy_user_pass': b'duoipvriezfde:bq4RYrQiWuQzv'},
        ]

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_info)
        request.meta['proxy'] = proxy['proxy_url']
        proxy_user_pass = proxy['proxy_user_pass']
        encoded_user_pass = base64.b64encode(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass.decode()
        # return None
