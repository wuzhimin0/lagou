# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positions = Field()
    salary = Field()
    company_name = Field()
    # 城市
    city = Field()
    # 地区
    district = Field()
    # 工作经验
    workYear = Field()
    # 学历
    education = Field()
    # 工作标签
    industryLables = Field()
    # 工作详情
    job_detail = Field()
    # 公司在拉勾网上的网址
    company_url = Field()
