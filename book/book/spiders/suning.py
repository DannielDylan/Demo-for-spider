# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SuningSpider(CrawlSpider):
    name = 'suning'
    allowed_domains = ['suning.com']
    # start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']
    start_urls = ['http://snbook.suning.com/web/trd-fl/100301/46.htm']

    rules = (
        #提取列表页的url地址
        Rule(LinkExtractor(allow=r'/web/trd-fl/\d+/\d+.htm$'), callback="parse_next_url",follow=True),
        #提取图书详情页的url地址
        Rule(LinkExtractor(allow=r'/web/prd/\d+.htm$'),callback="parse_item" ,follow=True),
        #
    )

    def parse_next_url(self,response):
        print("*" * 100)
        print(response.request.headers["User-Agent"])
        '''
        var
        pagecount = 103;
        var
        currentPage = 2;
        '''
        #提取图书详情页的数据
        url_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li/div[1]/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(
                url,
                callback=self.parse_item
            )

        #列表页翻页
        current_page = re.findall(r"var currentPage=(.*?);",response.body.decode())
        current_page = int(current_page[0]) if len(current_page)>0 else 0
        total_page = re.findall(r"var pagecount=(.*?);",response.body.decode())
        total_page = int(total_page[0]) if len(total_page) > 0 else 0
        if current_page<total_page:
            '''http://snbook.suning.com/web/trd-fl/100301/46.htm?pageNumber=2&sort=0'''
            next_url_temp = response.url.split("?")[0]
            next_url = next_url_temp + "?pageNumber={}&sort=0".format(current_page+1)
            #提取列表页的下一页的数据
            yield scrapy.Request(
                next_url,
                callback=self.parse_next_url
            )


    def parse_item(self, response):
        item = {}
        item["cate_info"] = response.xpath("//div[@class='bread']/div/a/text()").extract()
        item["cate_href"] =  response.xpath("//div[@class='bread']/div/a/@href").extract()
        item["book_name"] = response.xpath("//div[@class='bread']/div/span[last()]/text()").extract_first()
        item["book_price"] = re.findall(r"\"bp\":'(.*?)'",response.body.decode())
        item["book_price"] = item["book_price"][0] if len(item["book_price"])>0 else None
        item["book_press"] = response.xpath("//em[text()='出 版 社']/../../a/text()").extract_first()
        item["book_author"] = response.xpath("//a[@name='snprd_xx_spzs_author02']/text()").extract_first()
        item["book_publish_date"] = response.xpath("//em[text()='出版日期']/../../span[2]/text()").extract_first()
        item["book_desc"] = response.xpath("//h3[text()='内容简介']/../div/p/text()").extract()
        item["book_href"] = response.url
        print(item)
