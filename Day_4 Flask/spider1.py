'''
Author: skilywen
Date: 2024-06-06 13:37:45
'''

"""
    1.爬取所有页面的电影信息
    2.将信息以json数据的格式存入本地
    3.多线程
    ==============================
    流程:
    1. 获取所有的电影的URL
    2. 解析每一个电影的html页面
    3. 将获取的数据写入到本地的json文件中
"""
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import queue
import threading
import time



# https://ssr1.scrape.center/page/2
URL = 'https://ssr1.scrape.center'
PAGE = 10
PATH = './moveis' #定义爬取数据存放的目录  PATH + '/' + 
if not os.path.exists(PATH):
    os.mkdir(PATH)

Q = queue.Queue()
def get_a():
    """
    获取所有 a 标签中的电影链接
    """
    for page in range(1, PAGE+1):
        #每一页 url 链接 f'{URL}/page/{page}'
        url = URL + '/page/' + str(page)
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        html = res.text

        soup = BeautifulSoup(html, 'html.parser')
        #获取每一页中的 a 标签链接
        atags = soup.find_all('a', {'class':'name'})
        # print([atag['href'] for atag in atags])
        #将电影的url存入队列中
        for atag in atags:
            Q.put(URL + atag['href'])

# get_a()
def get_content(url):
    """
    获取电影的详细信息
    """
    try:
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        html = res.text

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.h2.string
        # print(title)
        # categories = [span.string for span in soup.find('div', {'class':'categories'}).findAll('span')]
        # for cateogrie_div in categories_div:
        #1. 所有的class为info的div标签 2. 通过div 再定位到span标签 
        # info_divs1, info_divs2 = soup.findAll('div', {'class':'info'})
        # info_spans1 = info_divs1.findAll('span')
        # countries = info_spans1[0].string
        # time = info_spans1[-1].string
        # published = info_divs2.span.string
        # drama = soup.find('div', {'class':'drama'}).p.string.strip()
        # score = soup.find('p', {'class':'score'}).string.strip()

        #正则表达式提取数据 => 切片
        categories = re.findall(r'<span>(.*)</span>', html)[:-1]
        countries = re.search(r'">([^\x00-\xff]+)</span>', html).group(1) if re.search(r'">([^\x00-\xff]+)</span>', html) else ''
        time = re.search(r'>(\d+.*)</span>', html).group(1) if re.search(r'>(\d+.*)</span>', html) else ''
        published = re.search(r'\d+-\d+-\d+', html).group() if re.search(r'\d+-\d+-\d+', html) else ''
        drama = re.search(r'>\s+(.*)\s+</p>', html).group(1) if re.search(r'>\s+(.*)\s+</p>', html) else ''
        score = re.search(r'\d+\.\d+', html).group() if  re.search(r'\d+\.\d+', html) else ''
        # print(title, categories, countries, time,published,drama,score)

        dic = {
            'title':title,
            'categories':categories,
            'time':time,
            'published':published,
            'drama':drama,
            'score':score
        }
        return dic
    except Exception as e:
        print(url)
    

def write_content():
    """
    线程任务函数
    """
    while not Q.empty():
        url = Q.get()
        content_dic = get_content(url)
        #PATH + '/' + content_dic['title'] + '.json'
        #字典不能直接写入文本中 
        #字典 => json json.dumps()
        #josn => 字典  json.loads()
        with open(os.path.join(PATH, content_dic['title']), 'w', encoding='utf8') as f:
            data = json.dumps(content_dic, ensure_ascii=False)
            f.write(data)

def start_thread(thread_names, thread_nums, args=tuple()):
    """
    线程启动函数
    params: thread_names function 线程函数
    params: thread_nums  int  线程的数量
    params: args tuple 线程函数的参数
    """
    threads = []
    for i in range(thread_nums):
        t = threading.Thread(target=thread_names, args=args)
        t.setDaemon(True)
        t.start()
        threads.append(t)

    #主线程等待子线程结束
    # for t in threads:
    #     t.join()
    alive = True
    while alive:
        alive = False
        for t in threads:
            #is_alive 可以判断线程是否是活跃
            if t.is_alive():
                alive = True
        time.sleep(0.1)

# def main()


if __name__ == '__main__':
    get_a()
    start_thread(write_content, 5)



# get_content('https://ssr1.scrape.center/detail/13')
# write_content('https://ssr1.scrape.center/detail/13')

