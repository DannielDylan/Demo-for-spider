# coding=utf-8
from selenium import webdriver
import time

class Douyu:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    def get_content_list(self):
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        content_list = []
        for li in li_list:
            item = {}
            item["img"] = li.find_element_by_xpath(".//span[@class='imgbox']/img[last()]").get_attribute("src")
            item["room_name"] = li.find_element_by_xpath("./a").get_attribute("title")
            item["cate_name"] = li.find_element_by_xpath(".//div[@class='mes-tit']/span").text
            item["watch_num"] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
            item["anchor_num"] = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
            print(item)
            content_list.append(item)

        next_url = self.driver.find_elements_by_class_name("shark-pager-next")
        next_url = next_url[0] if len(next_url)>0 else None
        return  content_list,next_url

    def save_content_list(self,content_list):
        with open("douyu.csv",'w',encoding='utf-8') as file:
            file.write(content_list)

    def __del__(self):
        self.driver.quit()

    def run(self):


        self.driver.get(self.start_url)

        content_list,next_url = self.get_content_list()

        self.save_content_list(content_list)

        while next_url is not None:
            next_url.click()
            time.sleep(2)
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)
        # self.driver.quit()

if __name__ == '__main__':
    douyu = Douyu()
    douyu.run()