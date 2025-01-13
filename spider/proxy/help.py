from pydantic import BaseModel, Field
from typing import Optional

class IpInfoModel(BaseModel):
    """Unified IP model"""
    ip: str = Field(title="ip")
    port: int = Field(title="端口")
    user: str = Field(title="IP代理认证的用户名")
    protocol: str = Field(default="https://", title="代理IP的协议")
    # default：字段的默认值。如果未提供值，则使用默认值。
    # title：字段的描述，通常用于生成文档或增强可读性。
    # description：提供字段的详细描述。
    # example：提供字段的示例值，用于文档生成。
    # gt、lt、ge、le：设置数字字段的范围（如大于、少于等）。
    # regex：用于字符串字段的正则表达式验证。
    password: str = Field(title="IP代理认证用户的密码")
    expired_time_ts: Optional[int] = Field(title="IP 过期时间")
    #Optional[int]：表示这个字段是可选的（可以为 None 或 int 类型）。


#这段代码定义了一个类 IpInfoModel，继承自 BaseModel，通常是 Pydantic 的 BaseModel 类，
# 用于数据验证和序列化。
# 它被用来描述和验证一个IP信息的数据模型，如 IP 地址、端口号、用户名、密码等。

#可以变为.json   或者.dict

#1. BaseModel
# BaseModel 是来自 Pydantic 库的基类，用于定义数据模型。
# 它提供：
    # 数据验证：会自动检查字段值是否符合类型要求（如 ip 必须是字符串，port 必须是整数）。
    # 数据解析：可以将输入数据（如字典或 JSON）转换为 Python 对象。
    # 数据序列化：可以将模型对象转为字典或 JSON。
# 字段的详细含义
# 字段名	类型	描述
# ip	str	IP 地址，必须是字符串类型。
# port	int	端口号，必须是整数。
# user	str	代理认证的用户名。
# protocol	str	默认值为 "https://"，表示使用的协议。
# password	str	代理认证用户的密码。
# expired_time_ts	Optional[int]	可选字段，IP 的过期时间戳（整数或空）。



# 1. async 的含义
# async 是用来定义异步函数的关键字。
# 异步函数允许你在函数内部使用 await 来挂起（暂停）函数的执行，等待异步任务完成，而不会阻塞程序的运行。.
async def my_function():
    # 这是一个异步函数
    await asyncio.sleep(1)
    print("异步任务完成")
#2. await 的含义
# await 是用来挂起当前异步函数的执行，直到 await 的异步任务完成。
# 它只能在 async 定义的函数中使用。
# 在挂起期间，事件循环可以运行其他任务（实现并发）。
# result = await some_async_function()
#await 后面必须是一个异步对象，比如一个协程、asyncio.Future 或 asyncio.Task。

#3. async 和 await 的工作原理
# 当程序遇到 await 时，异步函数会将控制权交还给事件循环（Event Loop）。
# 事件循环可以运行其他任务，而不是等待当前任务完成。
# 一旦 await 的操作完成，程序会从暂停的位置继续执行。

import asyncio

async def task1():
    print("Task 1: Start")
    await asyncio.sleep(2)  # 挂起，等待 2 秒
    print("Task 1: End")

async def task2():
    print("Task 2: Start")
    await asyncio.sleep(1)  # 挂起，等待 1 秒
    print("Task 2: End")

async def main():
    await asyncio.gather(task1(), task2())  # 并发运行任务
    #异步函数 可以在其他异步函数中使用 await _is_valid_proxy() 来运行它。
# asyncio.run(main())

#asyncio.get_event_loop().run_until_complete(main_test(k))