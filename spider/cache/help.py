
#pickle.loads(value) 是 Python 中 pickle 模块 提供的函数，
# 用于将序列化后的二进制数据（字符串或字节流）反序列化回原始 Python 对象。

#pickle 模块简介
# pickle 是 Python 内置的模块，用于将 Python 对象序列化（保存为字节流）和反序列化（恢复为 Python 对象）。
# 序列化后的数据可以用于存储到文件、数据库，或通过网络传输。

# pickle.loads 的作用
    # loads 是 "load string" 的缩写。
    # 其作用是从一个二进制字节流中恢复出原始对象。
    # 参数 value 必须是 bytes（字节数据） 或 bytearray 类型。

import pickle

# 原始对象
data = {"name": "ChatGPT", "age": 3, "skills": ["Python", "AI"]}

# 1. 将对象序列化为字节流
serialized_data = pickle.dumps(data)  # dumps = "dump string"
print(f"序列化后的数据: {serialized_data}")

# 2. 将序列化的字节流反序列化回原始对象
deserialized_data = pickle.loads(serialized_data)
print(f"反序列化后的数据: {deserialized_data}")


#loop = asyncio.get_event_loop() 是 Python asyncio 模块中的一个方法，
# 用于获取当前线程的 事件循环（Event Loop）。

#1. 事件循环（Event Loop）是什么？
    # 事件循环 是 asyncio 的核心机制之一。
    # 它负责管理和调度异步任务，确保异步代码能够并发运行，而不会阻塞主程序。
    # 异步任务通过事件循环执行，例如 await 语法、协程、asyncio 任务等。

# 2. asyncio.get_event_loop() 的作用
    # 获取当前线程的事件循环：
    # 如果当前线程已有事件循环，则返回该事件循环。
    # 如果当前线程没有事件循环，则会抛出 RuntimeError。
    # 在大多数情况下，get_event_loop() 用于获取默认的事件循环实例，以便运行异步任务。
import asyncio

# 获取当前线程的事件循环
loop = asyncio.get_event_loop()

async def say_hello():
    print("Hello, asyncio!")

# 通过事件循环运行协程
loop.run_until_complete(say_hello())  #Hello, asyncio!

# 在 Python 3.10+ 中的新推荐
# 从 Python 3.10 开始，推荐使用 asyncio.run() 而不是手动获取事件循环：
#
# python
# 复制代码
import asyncio

async def main():
    print("Hello, asyncio!")

# 直接运行异步函数
asyncio.run(main())
# 优点：
# asyncio.run 会自动创建事件循环并管理其生命周期。
# 避免手动获取和关闭事件循环的麻烦。

