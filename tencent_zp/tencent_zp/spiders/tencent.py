# -*- coding: utf-8 -*-
import scrapy
from tencent_zp.items import TencentZpItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']


    def parse(self, response):
        tr = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for td in tr:
            item = TencentZpItem()
            item['position_name'] = td.xpath('./td/a[@target="_blank"]/text()').extract()[0]
            item['position_link'] = td.xpath('./td[1]/a/@href').extract()[0]
            item['position_type'] = td.xpath('./td[2]/text()').extract()[0]
            item['zp_num'] = td.xpath('./td[3]/text()').extract()[0]
            # 工作地点
            item['workspace'] = td.xpath('./td[4]/text()').extract()[0]
            # 发布时间
            item['publish_time'] = td.xpath('./td[5]/text()').extract()[0]
        # next_page_url=response.xpath("//a[text()='下一页']/@href").extract()
        # while len(next_page_url)>0:
        #     #scrapy.Request能构建一个requests 同时指定提取数据的callback函数
        #     yield scrapy.Request(next_page_url,callback=self.parse)
        next_url_temp = response.xpath("//a[@id='next']/@href").extract_first()
        if next_url_temp is not None and next_url_temp != "javascript:;":
            next_url = "http://hr.tencent.com/" + next_url_temp

            yield scrapy.Request(next_url, callback=self.parse)