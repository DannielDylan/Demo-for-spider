#coding=utf-8
import time
import json
import requests
import pymongo
from pprint import pprint
from lxml import etree
from pymongo import MongoClient
from selenium import webdriver
from multiprocessing.dummy import Pool as ThreadPool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
class Netease(object):
    def __init__(self):
        self.base_url = "http://music.163.com/#/discover/playlist/"
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_window_size(1920, 1080)
        client = pymongo.MongoClient("localhost",27017)
        mydb = client.music
        self.db_category = mydb.category
        self.db_playlist = mydb.playlist
        self.db_track = mydb.track

    def get_category(self):
        self.driver.get(self.base_url)
        self.driver.switch_to_frame("g_iframe")
        temp = self.driver.find_elements_by_xpath('//*[@class="bd"]//a')
        temp = temp[1:]
        for i in temp:
            category_name = i.get_attribute("data-cat")
            print("name:",category_name)
            herf = i.get_attribute("href")
            print(herf)
            data = dict(
                name = category_name,
                href = herf,
                last_updated = time.strftime('%Y-%m-%d %H:%M:%S')
            )
            object_id = self.db_category.insert(data)

    def load_category(self):
        category_list = self.db_category.find()
        pool = ThreadPool(5)
        pool.map(self.start,category_list)
        pool.close()
        pool.join()

    def start(self,category):
        category_id = category.get("_id")
        category_href = category.get("href")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(1920, 1080)
        self.get_playlist_list(category_href,category_id,driver)
        driver.close()

    def get_playlist_list(self,category_href,category_id,driver):
        driver.get(category_href)
        time.sleep(2)
        driver.switch_to_frame('g_iframe')
        temp = driver.find_elements_by_xpath('//*[@id="m-pl-container"]/li/p[1]/a')
        for playlist in temp:
            playlist_href = playlist.get_attribute("href")
            self.get_playlist_detail(playlist_href,category_id)
        try:
            next_page = driver.find_element_by_xpath('//a[@class="zbtn znxt"]').get_attribute("href")
            print(next_page)
            return self.get_playlist_list(next_page,category_id,driver)
        except Exception as e:
            print(e)
            pass

    def get_playlist_detail(self,playlist_href,category_id):
        playlist_api = "http://music.163.com/api/playlist/detail?id=" + playlist_href.split("=")[-1]
        json_response = self.parse_api(playlist_api)
        playlist_detail = json_response.get("result")
        playlist_detail["category_id"] = category_id
        print(playlist_detail.get("name"))
        self.db_playlist.insert(playlist_detail)

    def load_playlist(self):
        pool = ThreadPool(5)
        category_id_temp = self.db_category.find()
        category_id_list = [i.get("_id") for i in category_id_temp]
        for category_id in category_id_list:
            print("category_id:",category_id)
            playlist_list = self.db_playlist.find({"category_id":category_id})
            pool.map(self.start_track,playlist_list)
        pool.close()
        pool.join()

    def start_track(self,playlist):
        category_id = playlist.get("category_id")
        playlist_id = playlist.get("_id")
        for track in playlist.get("tracks"):
            print(track.get("name"))
            track_id = track.get("id")
            track["category_id"] = category_id
            track["playlist_id"] = playlist_id
            track["lyric"] = self.parse_lyric(track_id)
            self.db_track.insert(track)

    def parse_lyric(self,track_id):
        track_url = "http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1".format(track_id)
        response = self.parse_api(track_url)
        if response is not None:
            try:
                response = self.json_loads(response.text)
                lyric_temp = response.get("lrc")
                if lyric_temp is not None:
                    lyric = lyric_temp.get("lyric")
                    if lyric is not None:
                        lyric = [i.split("]")[-1] for i in lyric.split("\n")]
                        return " ".join([i.strip() for i in lyric if i is not None])
                    else:
                        return None
                else:
                    return None
            except Exception as e:
                print(e)
                return None
        else:
            return None

    def parse_api(self,url):
        try:
            response = requests.get(url, timeout=60)
            i = 0
            while response.status_code != 200 and i<3:
                if response.status_code == 500:
                    return None
                print("now request the %s times"%i,url,response.text)
                response = requests.get(url,headers = headers, timeout=60)
                i+=1
            return response
        except Exception as e:
            return None

    def json_loads(self,response_str):
        try:
            json_response = json.loads(response_str)
        except Exception as e:
            json_response = None
            print("this is json.loads error",e,"has been ignored")
        return json_response

    def __exit__(self):
        pass

if __name__ == "__main__":
    a = Netease()
    a.get_category()
    a.load_category()
    a.load_playlist()
