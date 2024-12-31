import requests
from bs4 import BeautifulSoup
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'referer':'https://cn.bing.com/'
}
url='https://blog.51cto.com/u_16213344/12952732'
res = requests.get(url,headers=headers).text
soup = BeautifulSoup(res,'html.parser')
print(soup.select('pre > code')[0].text)