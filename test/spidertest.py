# coding:utf-8


import re
import urlparse
import requests
from bs4 import BeautifulSoup


# BeautifulSoup内置了一些查找方法 ，常用的find() find_all() find_parent() find_parents() find_next_sibling()  find_next_siblings() find_next()  find_all_next()


class SpiderTest(object):
    def __init__(self):
        print 'hello python'

    def parseHtml(self):
        url = 'http://m.ctrip.com'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
        r = requests.post(url, headers=headers)
        # print r.request.headers  打印请求头信息
        # print r.content  打印html内容


        htmlCon = r.content
        soup = BeautifulSoup(htmlCon,'html.parser')


        # find()  find()用来查找第一个匹配结果出现的地方
        # 通过标签查找
        # content = soup.find("em")
        # print content.get_text()


        # 通过文本查找
        # content = soup.find(text="团购")
        # print content


        # 通过正则表达式查找   输出  abc@example.com
        # email_id_example = """<br/>
        #         <div>The below HTML has the information that has email ids.</div>
        #         abc@example.com
        #         <div>xyz@example.com</div>
        #         <span>foo@example.com</span>
        #         """
        # soup = BeautifulSoup(email_id_example, "html.parser")
        # emailid_regexp = re.compile("\w+@\w+\.\w+")
        # first_email_id = soup.find(text=emailid_regexp)
        # print first_email_id


        # 通过标签属性进行查找
        # content = soup.find(id='c_hotel').find('em')
        # print content.get_text()

        # 基于CSS类的查找 因为class在python中是关键字  所以以class_来表示
        # content = soup.find(class_='row').find('em')
        # print content.get_text()

        # 也可以使用这种方法
        # content = soup.find(attrs={'class':'row'}).find('em')
        # print content.get_text()



        # find_all() 找到所有匹配结果出现的地方
        # contents = soup.find_all(class_='row')
        # for content in contents:
        #     print content.get_text()

        # find_all() 找到所有匹配结果出现的地方  limit=2 limit参数可以限制我们想要得到结果的数目
        contents = soup.find_all(class_='row',limit=5)
        for content in contents:
            print content.get_text()



if __name__ == "__main__":
    spiderTest = SpiderTest()
    spiderTest.parseHtml()
