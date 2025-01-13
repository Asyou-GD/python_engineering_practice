import asyncio
import time
from multiprocessing import freeze_support

import spider.cache.local_cache
from spider.proxy.proxy_ip_pool import ProxyIpPool
from spider import config
import requests
from spider.cache import local_cache
from spider.proxy import IpInfoModel
from spider.proxy.proxy_ip_pool import create_ip_pool

config.ENABLE_IP_PROXY = True

async def test_proxy(proxy):
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

async def GetProxy() -> ProxyIpPool:
    if config.ENABLE_IP_PROXY:
        ip_proxy_pool = await create_ip_pool(
            config.IP_PROXY_POOL_COUNT, enable_validate_ip=True
        )
        ip_proxy_info: IpInfoModel = await ip_proxy_pool.get_proxy()
        httpx_proxy_format = ip_proxy_pool.format_proxy_info(ip_proxy_info)
        return ip_proxy_pool, httpx_proxy_format


async def main():
    ip_proxy_pool, httpx_proxy_format = await GetProxy()
    print(httpx_proxy_format)

    # 依次调用异步任务
    await test_proxy(httpx_proxy_format)
    await ip_proxy_pool.ip_provider.ip_cache.cache_client.stop()
if __name__ == '__main__':
    asyncio.run(main())  # type:ProxyIpPool

    test_url = "http://httpbin.org/ip"
    print(f"无代理")
    # 发送 GET 请求，通过代理访问测试 URL
    response = requests.get(test_url, timeout=5)
    print( response.json().get("origin"))

