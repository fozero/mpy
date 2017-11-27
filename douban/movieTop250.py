# coding:utf-8
import re
import urlparse
import requests
from bs4 import BeautifulSoup


# 爬取豆瓣电影TOP250数据   电影信息  评分 以及用户评论
# python版本2.7
class Movie(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def get_top250_url(self,root_url):
        nums = 0
        while nums<=250:
            try:
                param = {'start': nums, filter: ''}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
                resp = requests.post(root_url, headers=headers, data=param)
                soup = BeautifulSoup(resp.content, 'html.parser', from_encoding='utf-8')
                # links = soup.find_all('a', href=re.compile(r'/subject/'))  # re.compile(r'/subject/') 正则匹配
                links = soup.find(class_='article').find_all('a', href=re.compile(r'/subject/'))  # re.compile(r'/subject/') 正则匹配

                for link in links:
                    detail_url = link['href']
                    self.add_new_url(detail_url)
                    print detail_url

                nums = nums + 25
            except:
                print 'fail'

    def get_movie_data(self):
        while self.has_new_url():
            try:
                new_url = self.get_new_url()
                html_con = self.download(new_url)
                data = self.parse(new_url,html_con)
                print data
            except:
                print 'craw failed'

    # 抓取
    def craw(self,root_url):
        # 第一步获取首页所有的链接  将其添加到url管理器中
        self.get_top250_url(root_url)

        # 第二步 遍历所有的url地址 获取电影相关信息 评分以及用户评论
        self.get_movie_data()


    # 下载页面
    def download(self,url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = r.content
        return res


    # 解析
    def parse(self,new_url,html_con):
        res_data = {}

        # 当前页面url地址
        res_data['new_url'] = new_url
        soup = BeautifulSoup(html_con, 'html.parser', from_encoding='utf-8')

        # 电影标题
        title = soup.find(id='content').find('h1').get_text()
        res_data['title'] = title

        # 电影封面
        img = soup.find(class_='subject').find('img')['src']
        res_data['img'] = img

        # 评分
        score = soup.find(class_='rating_num').get_text()
        res_data['score'] = score

        # 评论数
        comment_num = soup.find(class_='rating_people').find('span').get_text()
        res_data['comment_num'] = comment_num

        # 电影简介
        intro = soup.find(class_='related-info').find(attrs = {'property':'v:summary'}).get_text()
        res_data['intro'] = intro

        # 影评url地址
        _comment_url = soup.find('p',class_='pl').find('a')['href']
        # urljoin基地址和相对地址的拼接
        comment_url = urlparse.urljoin(new_url,_comment_url)
        res_data['comment_url'] = comment_url

        return res_data


    # 添加新地址
    def add_new_url(self,url):
        self.new_urls.add(url)

    # 获取地址
    def get_new_url(self):
        new_url = self.new_urls.pop()  # pop()移除列表中的一个元素
        self.old_urls.add(new_url)
        return new_url

    # 是否还有新url
    def has_new_url(self):
        return len(self.new_urls) != 0

if __name__ == "__main__":
    # https://movie.douban.com/top250?start=25&filter=
    root_url = 'https://movie.douban.com/top250'
    movie = Movie()
    movie.craw(root_url)