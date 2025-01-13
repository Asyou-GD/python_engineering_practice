# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2023/12/2 13:45
# @Desc    : ip代理池实现
import random
from typing import List
import re
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from spider import config
from spider.proxy.providers import new_jisu_http_proxy, new_kuai_daili_proxy
from spider.tools import utils

from .types import IpInfoModel, ProviderNameEnum
from spider.proxy.providers import kuaidl_proxy
from typing import Optional, Dict


class ProxyIpPool:
    def __init__(self, ip_pool_count: int,
                 enable_validate_ip: bool,
                 ip_provider
                 ) -> None:
        """

        Args:
            ip_pool_count:
            enable_validate_ip:
            ip_provider:
        """

        self.ip_pool_count = ip_pool_count
        self.enable_validate_ip = enable_validate_ip
        self.proxy_list: List[IpInfoModel] = []
        self.ip_provider = ip_provider  # type: kuaidl_proxy.KuaiDaiLiProxy

    async def load_proxies(self) -> None:
        """
        加载IP代理
        Returns:

        """
        self.proxy_list = await self.ip_provider.get_proxies(self.ip_pool_count)
        print('共',len(self.proxy_list),'个代理------')
        self.ip_provider.ip_cache.save_all_ip()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
    async def get_proxy(self) -> IpInfoModel:
        """
        从代理池中随机提取一个代理IP
        :return:
        """
        if len(self.proxy_list) == 0:
            await self._reload_proxies()

        proxy = random.choice(self.proxy_list)
        self.proxy_list.remove(proxy)  # 取出来一个IP就应该移出掉

        if self.enable_validate_ip:
            if not await self.ip_provider.valid_proxy(proxy):
                raise Exception("[ProxyIpPool.get_proxy] current ip invalid and again get it")
        return proxy

    async def saveredis(self, ip_proxy_pool) -> None:
        await self._reload_proxies()

        ip_proxy_list = []
        while len(self.proxy_list) != 0:
            ip_proxy_info: IpInfoModel = await ip_proxy_pool.get_proxy()
            httpx_proxy_format = self.format_proxy_info(ip_proxy_info)
            ip_proxy_list.append(httpx_proxy_format)

        self.Redis_db.set('ip', ip_proxy_list)

    async def loadredis(self) -> list:
        ip_proxy_list = self.Redis_db.get("ip")
        return ip_proxy_list

    def format_proxy_info(self, ip_proxy_info: IpInfoModel, ) -> \
            Optional[Dict]:
        """format proxy info for playwright and httpx"""
        playwright_proxy = {
            "server": f"{ip_proxy_info.protocol}{ip_proxy_info.ip}:{ip_proxy_info.port}",
            "username": ip_proxy_info.user,
            "password": ip_proxy_info.password,
        }
        httpx_proxy = {
            "http":  f"http://{ip_proxy_info.user}:{ip_proxy_info.password}@{ip_proxy_info.ip}:{ip_proxy_info.port}",
            "https": f"http://{ip_proxy_info.user}:{ip_proxy_info.password}@{ip_proxy_info.ip}:{ip_proxy_info.port}"
        }
        return httpx_proxy

    async def _reload_proxies(self):
        """
        # 重新加载代理池
        :return:
        """
        self.proxy_list = []
        await self.load_proxies()


IpProxyProvider = {
    ProviderNameEnum.JISHU_HTTP_PROVIDER.value: new_jisu_http_proxy(),
    ProviderNameEnum.KUAI_DAILI_PROVIDER.value: new_kuai_daili_proxy()
}


async def create_ip_pool(ip_pool_count: int, enable_validate_ip: bool) -> ProxyIpPool:
    """
     创建 IP 代理池
    :param ip_pool_count: ip池子的数量
    :param enable_validate_ip: 是否开启验证IP代理
    :return:
    """
    pool = ProxyIpPool(ip_pool_count=ip_pool_count,
                       enable_validate_ip=enable_validate_ip,
                       ip_provider=IpProxyProvider.get(config.IP_PROXY_PROVIDER_NAME)
                       )
    await pool.load_proxies()
    return pool


if __name__ == '__main__':
    pass
