import json
import re
import json
import requests
from bs4 import BeautifulSoup
import re

import requests


def test_proxy(proxy):
    """
    测试代理是否可用。
    :param test_url: 测试 URL（默认使用 httpbin.org 提供的 IP 测试服务）
    :return: None
    """
    test_url = "http://httpbin.org/ip"
    try:
        print(f"Testing proxy: {proxy}")
        # 发送 GET 请求，通过代理访问测试 URL
        response = requests.get(test_url, proxies=proxy, timeout=5)

        # 打印返回的 IP 地址
        if response.status_code == 200:
            print("Proxy is working!")
            print("Your IP via proxy is:", response.json().get("origin"))
            print()
        else:
            print(f"Failed to connect using proxy. Status code: {response.status_code}")
            print()
    except requests.exceptions.RequestException as e:
        print(f"Proxy failed: {e}")
        print()



headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'referer':'https://www.kuaidaili.com/free'
}
url = 'https://www.kuaidaili.com/free/dps/1/'
res = requests.get(url,headers=headers).text
soup = BeautifulSoup(res,'html.parser')

data_cover_url = soup.select('body > script:nth-child(9)')[0]
urls = re.search('.*?const fpsList = (.*?);',data_cover_url.text,re.S).groups()[0]
proxies = json.loads(urls)
# 示例代理列表（可替换为你自己的代理地址）

for proxy in proxies:
    proxy = {
        "http": f"http://{proxy['ip']}:{proxy['port']}",
        "https": f"http://{proxy['ip']}:{proxy['port']}"
    }  # 示例本地代理
    # 测试代理
    test_proxy(proxy)