# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import json
import random


class MafengwoProxyMiddleware(object):

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
