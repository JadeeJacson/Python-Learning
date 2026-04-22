# ============================================================
# Python 异步编程完全指南
# asyncio / async&await / 事件循环 / 协程 / Task / gather
# ============================================================

import asyncio
import time

# ============================================================
# 【核心概念】异步 vs 多线程 vs 多进程
# ============================================================
# 先搞清楚"为什么需要异步"：
#
# 同步代码：一件事没做完，下一件事等着          → 串行，慢
# 多线程：  多个线程各做一件事，靠OS切换         → 有线程开销，有GIL
# 异步：    单线程内，"等待"期间主动让出控制权   → 几乎零切换开销
#
# 核心比喻：
#   同步 = 你在奶茶店，下单后傻站着等，拿到才点下一杯
#   多线程 = 派3个人去3个奶茶店同时排队
#   异步 = 你下单后去刷手机，店员叫号了你再去取 ← 一个人搞定

# ============================================================
# 【1】协程（Coroutine）—— 异步的基本单位
# ============================================================
# 用 async def 定义的函数 = 协程函数
# 调用协程函数 不会立即执行，返回的是一个协程对象
# 必须被 await 或放入事件循环才会真正执行

async def say_hello():
    print("  Hello")
    await asyncio.sleep(1)      # ← 关键！遇到 await 主动交出控制权
    print("  World")            #   asyncio.sleep 不阻塞线程，只是"等1秒后继续"
    return "done"               # 协程可以有返回值

# 普通函数调用 vs 协程调用对比：
def normal_func(): return 42
result = normal_func()          # 直接执行，result = 42

coro = say_hello()              # 仅创建协程对象，函数体一行都没执行！
print(f"  协程对象: {coro}")    # <coroutine object say_hello at 0x...>
coro.close()                    # 手动关闭，避免"coroutine was never awaited"警告


# ============================================================
# 【2】事件循环（Event Loop）—— 异步的调度中心
# ============================================================
# 事件循环是异步程序的"大脑"：
#   - 维护一个任务队列
#   - 不断检查哪些任务可以继续执行（等待结束了）
#   - 调度执行，遇到 await 就切换到其他任务
#
# asyncio.run() 是最标准的入口，内部做了三件事：
#   1. 创建新的事件循环
#   2. 运行传入的协程直到完成
#   3. 关闭事件循环并清理

print("\n" + "=" * 55)
print("【2】事件循环基本运行")
print("=" * 55)

async def main_basic():
    print("  事件循环启动")
    result = await say_hello()  # await = 等这个协程跑完再继续
    print(f"  协程返回值: {result}")

asyncio.run(main_basic())       # ✅ Python 3.7+ 推荐写法，程序入口唯一的 run


# ============================================================
# 【3】await —— 让出控制权的开关
# ============================================================
# await 只能在 async def 函数内使用
# await 后面跟"可等待对象"：协程 / Task / Future
# 遇到 await：当前协程暂停 → 事件循环去干别的 → 等待完成后回来继续

print("\n" + "=" * 55)
print("【3】await 并发效果演示")
print("=" * 55)

async def fetch_data(name, delay):
    """模拟网络请求"""
    print(f"  [{name}] 开始请求...")
    await asyncio.sleep(delay)          # 模拟网络 I/O，期间让出控制权
    print(f"  [{name}] 请求完成！")
    return f"{name}_result"

async def main_sequential():
    """顺序 await：一个完成再开始下一个，总耗时 = 相加"""
    start = time.time()
    r1 = await fetch_data("API-1", 2)
    r2 = await fetch_data("API-2", 1)
    print(f"  顺序执行耗时: {time.time()-start:.1f}s，结果: {r1}, {r2}")
    # 耗时约 3s：2+1

asyncio.run(main_sequential())


# ============================================================
# 【4】Task —— 让协程真正并发
# ============================================================
# 直接 await 协程是顺序执行的（上面已证明）
# asyncio.create_task() 把协程包装成 Task，立刻加入事件循环调度
# Task 创建后会"在后台"推进，不需要等你 await 它

print("\n" + "=" * 55)
print("【4】Task 并发执行")
print("=" * 55)

async def main_concurrent():
    start = time.time()

    # create_task 立刻把两个协程都丢进事件循环
    # 注意：task 创建后就开始调度了，不是等到 await 才开始！
    task1 = asyncio.create_task(fetch_data("API-1", 2))
    task2 = asyncio.create_task(fetch_data("API-2", 1))

    # await task 时，事件循环会在两个任务间切换
    r1 = await task1
    r2 = await task2
    print(f"  并发执行耗时: {time.time()-start:.1f}s，结果: {r1}, {r2}")
    # 耗时约 2s：取最长的那个 ← 这才是异步并发的威力

asyncio.run(main_concurrent())

# Task 常用方法速查：
# task = asyncio.create_task(coro())  → 创建并调度任务
# await task                          → 等待任务完成，获取返回值
# task.done()                         → 是否已完成
# task.result()                       → 获取结果（未完成会抛异常）
# task.cancel()                       → 取消任务（会在 await 处抛 CancelledError）
# task.add_done_callback(fn)          → 任务完成时的回调


# ============================================================
# 【5】gather —— 并发执行多个协程，最常用！
# ============================================================
# asyncio.gather(*coros_or_tasks) 做三件事：
#   1. 把所有协程自动包装成 Task
#   2. 并发运行它们
#   3. 等全部完成，按原始顺序返回结果列表

print("\n" + "=" * 55)
print("【5】gather 批量并发")
print("=" * 55)

async def main_gather():
    start = time.time()

    # 最简洁的并发写法：直接传协程，gather 自动创建 Task
    results = await asyncio.gather(
        fetch_data("API-1", 2),
        fetch_data("API-2", 1),
        fetch_data("API-3", 3),
    )
    # results 顺序和传入顺序一致，不是完成顺序！
    print(f"  gather 结果: {results}")
    print(f"  gather 耗时: {time.time()-start:.1f}s")  # 约 3s：取最长

asyncio.run(main_gather())


# gather 异常处理：return_exceptions=True
async def risky_task(name, should_fail):
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError(f"{name} 失败了")
    return f"{name} 成功"

async def main_gather_exception():
    print("\n  --- gather 异常处理 ---")

    # 默认：任意一个抛异常，gather 立刻传播异常，其他任务继续但结果被丢弃
    # return_exceptions=True：把异常当作正常返回值，全部跑完再返回
    results = await asyncio.gather(
        risky_task("task1", False),
        risky_task("task2", True),   # 这个会失败
        risky_task("task3", False),
        return_exceptions=True       # ← 异常不会中断其他任务
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  ❌ 异常: {r}")
        else:
            print(f"  ✅ 成功: {r}")

asyncio.run(main_gather_exception())


# ============================================================
# 【6】综合实战：异步爬虫模拟（最贴近真实场景）
# ============================================================
print("\n" + "=" * 55)
print("【6】综合实战：异步模拟爬取10个URL")
print("=" * 55)

import random

async def async_fetch(session_id, url_id):
    """模拟异步 HTTP 请求（真实场景用 aiohttp 替换 asyncio.sleep）"""
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    return {"url_id": url_id, "status": 200, "size": random.randint(1000, 9999)}

async def main_crawler():
    start = time.time()

    # 并发爬取 10 个 URL
    tasks = [async_fetch("session", i) for i in range(10)]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    total_size = sum(r["size"] for r in results)
    print(f"  爬取完成: {len(results)} 个页面")
    print(f"  总耗时:   {elapsed:.2f}s（串行需要约 {sum(r['size']//1000 for r in results)+5}s）")
    print(f"  总大小:   {total_size} bytes")

asyncio.run(main_crawler())


# ============================================================
# 【7】asyncio 其他常用 API 速查
# ============================================================
async def demo_other_apis():

    # --- asyncio.wait_for：加超时控制 ---
    try:
        result = await asyncio.wait_for(fetch_data("超时测试", 5), timeout=2.0)
    except asyncio.TimeoutError:
        print("  ⏰ 请求超时！")

    # --- asyncio.sleep(0)：主动让出控制权，常用于长计算中"插空"调度 ---
    for i in range(3):
        await asyncio.sleep(0)      # 让事件循环有机会处理其他任务
        print(f"  计算步骤 {i}")

    # --- asyncio.current_task()：获取当前 Task ---
    task = asyncio.current_task()
    print(f"  当前任务: {task.get_name()}")

asyncio.run(demo_other_apis())