# ============================================================
# Python 并发工具：concurrent.futures 核心讲解
# ThreadPoolExecutor（线程池）& ProcessPoolExecutor（进程池）
# ============================================================

# ───────────────────────────────────────────────────────────
# 【核心概念】费曼理解法
# ───────────────────────────────────────────────────────────
# 想象你是餐厅老板，有一堆订单要处理：
#
# 单线程  = 你一个人处理所有订单，做完一个才做下一个
# 线程池  = 你雇了几个服务员（线程），大家共享同一个厨房（内存）
#            → 适合"等待型"任务：网络请求、文件读写（IO密集型）
# 进程池  = 你开了几个独立分店（进程），每家有自己的厨房（内存）
#            → 适合"计算型"任务：数据处理、图像压缩（CPU密集型）
#
# concurrent.futures 就是帮你"调度服务员/分店"的管理系统

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import os

# ───────────────────────────────────────────────────────────
# Part 1：ThreadPoolExecutor —— IO密集型任务
# 模拟场景：批量爬取URL（用sleep模拟网络延迟）
# ───────────────────────────────────────────────────────────

def fetch_url(url):
    """模拟网络请求，IO等待期间线程可以切换去做别的事"""
    time.sleep(0.5)  # 模拟网络延迟
    return f"[线程 {os.getpid()}] 抓取完成: {url}"

urls = [f"https://example.com/page/{i}" for i in range(6)]

print("=" * 55)
print("【线程池示例】IO密集型 - 模拟批量网络请求")
print("=" * 55)

start = time.time()

# with 语句会自动管理线程池的创建和销毁（重要！防止资源泄漏）
with ThreadPoolExecutor(max_workers=3) as executor:  # max_workers=3：同时最多3个线程

    # 方式一：map() —— 最简洁，保证结果顺序与输入一致
    # 类似内置 map()，但在线程池中并发执行
    results = list(executor.map(fetch_url, urls))
    for r in results:
        print(r)

print(f"\n耗时: {time.time() - start:.2f}s（串行需 ~3s，并发只需 ~0.5s）\n")

# ───────────────────────────────────────────────────────────
# Part 2：submit() + as_completed() —— 谁先完成谁先处理
# 场景：任务耗时不同，想第一时间拿到结果（比如竞速查询）
# ───────────────────────────────────────────────────────────

def task_with_delay(n):
    time.sleep(n * 0.3)  # 耗时不同
    return f"任务{n}完成，耗时{n*0.3:.1f}s"

print("=" * 55)
print("【submit + as_completed】谁快谁先出结果")
print("=" * 55)

with ThreadPoolExecutor(max_workers=4) as executor:
    # submit() 提交单个任务，立即返回 Future 对象（占位符，代表"未来的结果"）
    futures = {executor.submit(task_with_delay, i): i for i in [3, 1, 4, 2]}

    # as_completed()：哪个Future先完成，就先返回哪个（不保证顺序！）
    for future in as_completed(futures):
        task_id = futures[future]
        try:
            result = future.result()  # 获取返回值；若任务抛异常，这里会重新抛出
            print(f"  ✓ {result}")
        except Exception as e:
            print(f"  ✗ 任务{task_id}出错: {e}")  # 异常不会静默消失，需要显式处理

# ───────────────────────────────────────────────────────────
# Part 3：ProcessPoolExecutor —— CPU密集型任务
# 场景：大量数值计算（GIL限制下，多线程无法真正并行CPU计算！）
# ───────────────────────────────────────────────────────────

def cpu_heavy(n):
    """CPU密集型：纯计算，不涉及IO"""
    return sum(i * i for i in range(n))  # 模拟大量计算

# ⚠️ 重要：ProcessPoolExecutor 的代码必须在 if __name__ == "__main__" 保护下
# 原因：Windows下子进程会重新import主模块，不加保护会无限递归创建进程
if __name__ == "__main__":

    print("\n" + "=" * 55)
    print("【进程池示例】CPU密集型 - 并行数值计算")
    print("=" * 55)

    data = [10_000_000, 8_000_000, 12_000_000, 9_000_000]

    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:  # 一般设为CPU核心数
        results = list(executor.map(cpu_heavy, data))

    print(f"计算结果（前几位）: {[str(r)[:6]+'...' for r in results]}")
    print(f"进程池耗时: {time.time() - start:.2f}s")

    # 对比：单线程串行
    start = time.time()
    serial_results = [cpu_heavy(n) for n in data]
    print(f"串行耗时:   {time.time() - start:.2f}s")

# ───────────────────────────────────────────────────────────
# Part 4：Future 对象核心方法速查
# ───────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("【Future 对象常用方法】")
print("=" * 55)

with ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(lambda x: x ** 2, 10)

    print(f"done()  - 是否完成:    {future.done()}")       # 提交后立刻查，可能False
    result = future.result(timeout=5)                       # timeout防止永久阻塞！
    print(f"result()- 获取结果:    {result}")
    print(f"done()  - 完成后查询:  {future.done()}")        # True

# ───────────────────────────────────────────────────────────
# 【底层逻辑总结】
# ───────────────────────────────────────────────────────────
# ThreadPoolExecutor：
#   - 线程共享进程内存，切换开销小
#   - Python有GIL（全局解释器锁），同一时刻只有1个线程执行Python字节码
#   - IO等待时GIL会释放 → 多线程能真正并发IO操作
#   - 纯CPU计算时GIL不释放 → 多线程无法加速CPU任务（反而因切换更慢）
#
# ProcessPoolExecutor：
#   - 每个进程有独立GIL和内存空间
#   - 进程间通信靠序列化（pickle），传大对象有开销
#   - 真正多核并行，CPU密集任务加速明显
#   - 启动开销比线程大，不适合大量短小任务
#
# 选择口诀：等网络/磁盘 → 线程池；算矩阵/跑模型 → 进程池