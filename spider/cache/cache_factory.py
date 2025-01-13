from abc import ABC, abstractmethod
from typing import Any, List, Optional


#abc 是 Python 标准库中的一个模块，全称是 "Abstract Base Class"，即 抽象基类 模块。
#1. abc 模块的作用
    # abc 模块 提供了定义抽象基类（Abstract Base Class）的功能。
    # 抽象基类可以用来定义接口或约定，强制子类实现特定的方法。
    # 它的主要用途是提供一种结构化编程的方式，帮助开发者定义类的通用接口。
# 2. ABC 类
    # 在 abc 模块中，ABC 是所有抽象基类的基类。
    # 任何类只要继承自 ABC，就会成为抽象基类。
    # 如果在抽象基类中使用 @abstractmethod，则子类必须实现这个方法，否则无法实例化子类。
class AbstractCache(ABC):

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        -> Optional[Any]：这是返回类型提示，表示这个方法的返回值可以是任意类型，或者为 None。
        Union[Any, None]
        从缓存中获取键的值。
        这是一个抽象方法。子类必须实现这个方法。
        :param key: 键
        :return:
        """
        #raise NotImplementedError 用于在方法体内抛出一个未实现错误。
        #这表明该方法是抽象的，不能直接调用，需要在子类中提供具体实现。
        raise NotImplementedError


    @abstractmethod
    def set(self, key: str, value: Any, expire_time: int) -> None:
        """
        将键的值设置到缓存中。
        这是一个抽象方法。子类必须实现这个方法。
        :param key: 键
        :param value: 值
        :param expire_time: 过期时间
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def keys(self) -> List[str]:
        """
        获取所有符合pattern的key
        :return:
        """
        raise NotImplementedError

class CacheFactory:
    """
    缓存工厂类
    """

    @staticmethod
    def create_cache(cache_type: str, *args, **kwargs):
        """
        创建缓存对象
        :param cache_type: 缓存类型
        :param args: 参数
        :param kwargs: 关键字参数
        :return:
        """
        if cache_type == 'memory':
            from .local_cache import ExpiringLocalCache
            return ExpiringLocalCache(*args, **kwargs)
        elif cache_type == 'redis':
            from .redis_cache import RedisCache
            return RedisCache()
        else:
            raise ValueError(f'Unknown cache type: {cache_type}')
