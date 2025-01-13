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
# @Name    : 程序员阿江-Relakkes
# @Time    : 2024/6/2 11:05
# @Desc    : 本地缓存
import asyncio
import json
import threading
import time
from typing import Any, Dict, List, Optional, Tuple
from spider.config import base_config
from spider.cache.cache_factory import AbstractCache


class ExpiringLocalCache(AbstractCache):

    def __init__(self, cron_interval: int = 10):
        """
        初始化本地缓存
        :param cron_interval: 定时清楚cache的时间间隔
        :return:
        """
        self._cron_interval = cron_interval
        self._cache_container: Dict[str, Tuple[Any, float]] = {}
        self._stop = False
        self._clean_task = None
        self._initialize_cleaning_task()

    async def stop(self):
        """停止清理"""
        self._stop = True
        if self._clean_task:
            await self._clean_task

    def get(self, key: str) -> Optional[Any]:
        """
        从缓存中获取键的值
        :param key:
        :return:
        """
        value, expire_time = self._cache_container.get(key, (None, 0))
        if value is None:
            return None

        # 如果键已过期，则删除键并返回None
        if expire_time < time.time():
            del self._cache_container[key]
            return None

        return value

    def set(self, key: str, value: Any, expire_time: int = 180) -> None:
        """
        将键的值设置到缓存中
        :param key:
        :param value:
        :param expire_time: 过期时间 300s
        :return:
        """
        self._cache_container[key] = (value, time.time() + expire_time)

    def keys(self) -> List[str]:
        """
        获取所有符合pattern的key
        :param pattern: 匹配模式
        :return:
        """

        return list(self._cache_container.keys())

    def save_all_ip(self):
        json_data = self._cache_container
        with open(base_config.Local_cache, 'w', encoding='utf8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

    def load_all_ip(self):
        try:
            with open(base_config.Local_cache, 'r', encoding='utf8') as f:
                self._cache_container = json.load(f)
        except Exception as e:
            print('load err',e)

        self._clear()

    def _initialize_cleaning_task(self):
        try:
            loop = asyncio.get_running_loop()  # 获取当前运行的事件循环
            self._clean_task = loop.create_task(self._start_clear_cron())  # 创建任务
        except RuntimeError:
            # 如果没有运行中的事件循环，延迟启动
            asyncio.get_event_loop().call_soon(self._initialize_cleaning_task)

    def _clear(self):
        """
        根据过期时间清理缓存
        :return:
        """
        keys_to_delete = [key for key, (value, expire_time) in self._cache_container.items() if expire_time < time.time()]
        print('待清理key  ',keys_to_delete)
        for key in keys_to_delete:
            del self._cache_container[key]

    async def _start_clear_cron(self):
        """
        开启定时清理任务
        :return:
        """
        try:
            """定期清理过期数据"""
            while not self._stop:
                self._clear()
                await asyncio.sleep(self._cron_interval)  # 异步睡眠
        except Exception as e:
            print("定时清理任务已被取消",e)




if __name__ == '__main__':
    cache = ExpiringLocalCache(cron_interval=5)
    cache.start()

    cache.set("key1", "value1", expire_time=6)
    cache.set("key2", "value2", expire_time=10)
    cache.set("key3", "value3", expire_time=19)
    for _ in range(10):
        print(f"key1: {cache.get('key1')}, key2: {cache.get('key2')} key3: {cache.get('key3')}")
        time.sleep(2)

    cache.stop()
