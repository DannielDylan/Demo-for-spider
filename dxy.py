import datetime
import json
import random
import time
import requests
import pymongo
mongo_client=pymongo.MongoClient('mongodb://localhost:27017')
db=mongo_client['dingxiangyuan']
collection=db['collection']

class DxyArea:
    def __init__(self):
  
        # self.url="https://3g.jobmd.cn/s?wd={}&page={}".format(keyword,page)
        self.proxies={'http':"http://{}".format(self.get_proxy)}
        self.user_agent_list_mobile = ["Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36",
                              "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                              "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
                              "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, "
                              "like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
                              "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, "
                              "like Gecko) Chrome/62.0.3202.75 Mobile Safari/537.36",
                              "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) "
                              "Version/9.0 Mobile/13B143 Safari/601.1"]
        self.headers = {
        'user-agent': random.choice(self.user_agent_list_mobile)
    }

    def get_proxy(self):
        return requests.get("http://123.207.35.36:5010/get").text
    
    def _parse_url(self,start_url):
        data=requests.get(start_url,headers=self.headers,proxies=self.proxies).text
        dict=json.loads(data)
        return dict

    def parse_url(self,real_url):
        position_infos=requests.get(real_url,headers=self.headers,proxies=self.proxies).text
        dict=json.loads(position_infos)
        result = dict['results']['items']
        for each in result:
            # item=[]
            address = each['address']['address']
            address = address if len(address) > 0 else ""
            addressText = each['address']['addressText']
            province = each['address']['locationPinyin']
            location = each['address']['location']
            applyResumeCount = each['applyResumeCount']
            email = each['contactEmail']
            desc = each['descZh']
            # 应聘要求
            descZhSimple = each['descZhSimple']
            # 医院ID
            entId = each['entId']
            # 医院名称
            entName = each['entName']
            # 科室
            field1Text = each['field1Text']
            # 学历
            gradesText = each['gradesText']
            id = each['id']
            # 是否全职
            job = each['jobTypeText']
            # 工作年限要求
            jobYearText = each['jobYearText']
            # # 工资
            # max_salary=each['maxSalary']
            # min_salary=each['minSalary']
            salary = each['salaryText']
            # 职称
            name = each['name']
            # 科室名（英文）
            position1English = each['position1English']
            # 科室名（中文）
            position1Text = each['position1Text']
            # 医院规模
            scope = each['scope']
            # 医院性质
            typeName = each['typeName']
            # 福利待遇
            welfareEnums = each['welfareEnums']
            # 工作地点
            workLocationText = each['workLocationText']
            # position_infos=(address,addressText,)
            collection.insert({'address':address,"addressText":addressText,'province':province,"location":location,"applyResumeCount":applyResumeCount,"email":email,"desc":desc,"descZhSimple":descZhSimple,"entId":entId,'entName':entName,"field1Text":field1Text,"gradesText":gradesText,'id':id,'job':job,"jobYearText":jobYearText,"salary":salary,"name":name,"position1English":position1English,"position1Text":position1Text,"scope":scope,"typeName":typeName,"welfareEnums":welfareEnums,"workLocationText":workLocationText,"position_infos":position_infos})


    def read_max_page(self,dict):
        totalCount=dict['results']['pageBean']['totalCount']
        pageSize=dict['results']['pageBean']['pageSize']
        allpage=int(totalCount)/int(pageSize)+1
        # if page<allpage:
        #     page+=1
        return allpage

    def main(self):
        keyword=input("请输入你要查询职位:")
        # start_time=datetime.datetime.now()
        page=1
        start_url="https://3g.jobmd.cn/ajax/work/search?wd={}&page={}".format(keyword,page)
        dict=self._parse_url(start_url)
        allpage=self.read_max_page(dict)
        print(allpage)
        for page in range(1,int(allpage)):
            try:
                print("正在下载第{}页内容".format(page).center(50,'*'))
                real_url="https://3g.jobmd.cn/ajax/work/search?wd={}&page={}".format(keyword,page)
                self.parse_url(real_url)
                # self.save_tocsv(position_infos)
                time.sleep(random.randint(2,6))
            except Exception as e:
                print(e)

            
            
        



if __name__ == '__main__':
    dxy=DxyArea()
    dxy.main()
