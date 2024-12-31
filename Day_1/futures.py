import concurrent.futures
import time

def task(n):
    print(f"Starting task {n}")
    time.sleep(2)  # 模拟一个耗时的操作
    print(f"Task {n} completed")
    return n * 2

def main():
    start_time = time.time()
    tasks = list(range(5))  # 创建 5 个任务

    # 使用 ThreadPoolExecutor 来并行执行任务
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(task, tasks))

    end_time = time.time()
    print(f"Results: {results}")
    print(f"Total time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()