# -*- coding: utf-8 -*-
# 随机UserAgent和代理IP的所需库
import random
from scrapy.conf import settings
# 获取随机代理，自己写的
from proxypool.api import get_proxies
# UserAgent随机
class RandomUserAgent_Middleware(object):
    def __init__(self):
        # 35个UserAgent的列表
        self.user_agent_list = settings["USER_AGENT_LIST"]
    # 每次请求访问时，在headers中加入一个随机的UserAgent
    def process_request(self, request, spider):
        request.headers['USER_AGENT'] = random.choice(self.user_agent_list)
# 随机获取代理IP
class RandomProxy(object):
    def process_request(self,request,spider):
        # 每次访问时获取一个随机的代理IP
        request.meta["proxy"] = get_proxies()