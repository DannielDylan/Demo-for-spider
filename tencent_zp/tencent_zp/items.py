# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentZpItem(scrapy.Item):
    # define the fields for your item here like:
    #职位名称
    position_name = scrapy.Field()
    #职位类别
    position_type=scrapy.Field()
    #详情链接
    position_link=scrapy.Field()
    #招聘人数
    zp_num=scrapy.Field()
    #工作地点
    workspace=scrapy.Field()
    #发布时间
    publish_time=scrapy.Field()
    # pass


