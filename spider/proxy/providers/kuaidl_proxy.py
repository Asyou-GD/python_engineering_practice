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
# @Time    : 2024/4/5 09:43
# @Desc    : 快代理HTTP实现，官方文档：https://www.kuaidaili.com/?ref=ldwkjqipvz6c
import os
import re
from typing import Dict, List

import httpx
from pydantic import BaseModel, Field

from spider.proxy import IpCache, IpInfoModel
from spider.proxy.types import ProviderNameEnum
from spider.tools import utils


class KuaidailiProxyModel(BaseModel):
    ip: str = Field("ip")
    port: int = Field("端口")
    expire_ts: int = Field("过期时间")


def parse_kuaidaili_proxy(proxy_info: str) -> KuaidailiProxyModel:
    """
    解析快代理的IP信息
    Args:
        proxy_info:

    Returns:

    """
    proxies: List[str] = proxy_info.split(":")
    if len(proxies) != 2:
        raise Exception("not invalid kuaidaili proxy info")

    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5}),(\d+)'
    match = re.search(pattern, proxy_info)
    if not match.groups():
        raise Exception("not match kuaidaili proxy info")

    return KuaidailiProxyModel(
        ip=match.groups()[0],
        port=int(match.groups()[1]),
        expire_ts=int(match.groups()[2])
    )


class KuaiDaiLiProxy:
    def __init__(self, kdl_user_name: str, kdl_user_pwd: str, kdl_secret_id: str, kdl_signature: str):
        """

        Args:
            kdl_user_name:
            kdl_user_pwd:
        """
        self.kdl_user_name = kdl_user_name
        self.kdl_user_pwd = kdl_user_pwd
        self.api_base = "https://dps.kdlapi.com/"
        self.secret_id = kdl_secret_id
        self.signature = kdl_signature
        self.ip_cache = IpCache()
        self.proxy_brand_name = ProviderNameEnum.KUAI_DAILI_PROVIDER.value
        self.params = {
            "secret_id": self.secret_id,
            "signature": self.signature,
            "num":0,
            "pt": 1,
            "format": "json",
            "sep": 1,
            "f_et":1
        }
        self.valid_ip_url = "https://httpbin.org/ip"  # 验证 IP 是否有效的地址
        self.enable_validate_ip = True

    async def _is_valid_proxy(self, proxy: IpInfoModel) -> bool:
        """
        验证代理IP是否有效
        :param proxy:
        :return:
        """
        utils.logger.info(f"[ProxyIpPool._is_valid_proxy] testing {proxy.ip} is it valid ")
        try:
            httpx_proxy = {
                f"{proxy.protocol}": f"http://{proxy.user}:{proxy.password}@{proxy.ip}:{proxy.port}"
            }
            async with httpx.AsyncClient(proxies=httpx_proxy) as client:
                response = await client.get(self.valid_ip_url)
            if response.status_code == 200:
                utils.logger.info(f" testing {proxy.ip} 正常 ")
                return True
            else:
                utils.logger.info(f" testing {proxy.ip} 不正常 ")
                return False
        except Exception as e:
            utils.logger.info(f"[ProxyIpPool._is_valid_proxy] testing {proxy.ip} err: {e}")
            raise e

    async def valid_proxy(self,proxy):
        return await self._is_valid_proxy(proxy)

    async def get_proxies(self, num: int) -> List[IpInfoModel]:
        """
        快代理实现
        Args:
            num:

        Returns:

        """
        uri = "api/getdps/"

        # 优先从缓存中拿 IP
        ip_cache_list = self.ip_cache.load_all_ip()
        print('缓存中IP个数为',len(ip_cache_list))

        if len(ip_cache_list) >= num:
            return ip_cache_list[:num]

        # 如果缓存中的数量不够，从IP代理商获取补上，再存入缓存中
        need_get_count = num - len(ip_cache_list)
        self.params["num"] = need_get_count

        ip_infos: List[IpInfoModel] = []

        async with httpx.AsyncClient() as client:
            print('向远程获取ip')
            response = await client.get(self.api_base + uri, params=self.params)

            if response.status_code != 200:
                utils.logger.error(f"[KuaiDaiLiProxy.get_proxies] statuc code not 200 and response.txt:{response.text}")
                raise Exception("get ip error from proxy provider and status code not 200 ...")

            ip_response: Dict = response.json()

            if ip_response.get("code") != 0:
                utils.logger.error(f"[KuaiDaiLiProxy.get_proxies]  code not 0 and msg:{ip_response.get('msg')}")
                raise Exception("get ip error from proxy provider and  code not 0 ...")

            proxy_list: List[str] = ip_response.get("data", {}).get("proxy_list")
            for proxy in proxy_list:
                proxy_model = parse_kuaidaili_proxy(proxy)
                ip_info_model = IpInfoModel(
                    ip=proxy_model.ip,
                    port=proxy_model.port,
                    user=self.kdl_user_name,
                    password=self.kdl_user_pwd,
                    expired_time_ts=proxy_model.expire_ts,

                )
                ip_key = f"{self.proxy_brand_name}_{ip_info_model.ip}_{ip_info_model.port}"
                self.ip_cache.set_ip(ip_key, ip_info_model.model_dump_json(), ex=ip_info_model.expired_time_ts)
                ip_infos.append(ip_info_model)

            Ip_all = ip_cache_list + ip_infos
            print([self.ip_cache.cache_client.get(key) for key in self.ip_cache.cache_client.keys()])
            self.ip_cache.save_all_ip()
        return Ip_all


def new_kuai_daili_proxy() -> KuaiDaiLiProxy:
    """
    构造快代理HTTP实例
    Returns:

    """
    return KuaiDaiLiProxy(
        kdl_secret_id=os.getenv("kdl_secret_id", "oegnm4t8xvm6mq6315lm"),
        kdl_signature=os.getenv("kdl_signature", "naxjs704o6g3jw8ol2w9yt7vr36b6t4q"),
        kdl_user_name=os.getenv("kdl_user_name", "d2280261564"),
        kdl_user_pwd=os.getenv("kdl_user_pwd", "cuqtpqjq"),
    )

if __name__ == '__main__':
    async def main():
        a = new_kuai_daili_proxy()
        proxies = await a.get_proxies(1)
        print(proxies)

