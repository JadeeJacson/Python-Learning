# ============================================================
# Python 多进程完全指南
# multiprocessing / Process / Pool / Queue / Pipe
# ============================================================

import multiprocessing
import time
import os

# ============================================================
# 【核心概念】为什么需要多进程？
# ============================================================
# 上节课说了：GIL 让多线程无法并行执行 CPU 密集型任务
# 多进程的解决思路：每个进程有独立的 Python 解释器和 GIL
# → 4个进程 = 4把独立的锁 = 真正利用多核 CPU 并行计算
#
# 关键区别（面试必考）：
#   多线程：共享内存，通信方便，但有 GIL，适合 I/O 密集
#   多进程：独立内存空间，无 GIL，适合 CPU 密集，通信需要特殊机制
#
# 注意：Windows 下多进程必须放在 if __name__ == "__main__" 里！
# 原因：Windows 用 spawn 方式创建进程（重新导入模块），
#       没有保护会无限递归创建子进程 → 进程炸弹

# ============================================================
# 【1】Process —— 基础进程创建
# ============================================================

def cpu_task(name, n):
    """模拟 CPU 密集型任务：计算累加"""
    pid = os.getpid()           # 获取当前进程ID，证明真的是不同进程
    result = sum(range(n))
    print(f"  [{name}] PID={pid}, 计算结果={result}")

def demo_process():
    print("=" * 55)
    print("【1】Process 基本用法")
    print("=" * 55)

    # 和 Thread 用法几乎一样，直接替换类名即可
    p1 = multiprocessing.Process(target=cpu_task, args=("进程A", 10_000_000))
    p2 = multiprocessing.Process(target=cpu_task, args=("进程B", 10_000_000))

    start = time.time()
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(f"  两个进程并行耗时: {time.time()-start:.2f}s")

    # 对比串行
    start = time.time()
    cpu_task("串行1", 10_000_000)
    cpu_task("串行2", 10_000_000)
    print(f"  两个任务串行耗时: {time.time()-start:.2f}s")
    # 并行耗时约是串行的一半 ← 这就是多进程 vs 多线程处理CPU任务的优势

    # 常用属性速查：
    # p.pid          → 子进程的 PID（start() 后才有值）
    # p.exitcode     → 进程退出码，0 表示正常
    # p.is_alive()   → 是否还在运行
    # p.terminate()  → 强制终止进程（发送 SIGTERM）
    # p.daemon = True→ 守护进程，主进程退出时自动终止（start()前设置）


# ============================================================
# 【2】Pool —— 进程池（最常用！）
# ============================================================
# 每次创建/销毁进程开销很大（比线程重得多）
# Pool 预先创建好 N 个进程，复用它们处理任务，用完归还
# 就像"固定编制的工人团队"，而不是"每次临时招人"

def square(x):
    """计算平方，Pool 的 worker 函数必须定义在模块顶层"""
    return x * x

def heavy_compute(x):
    """模拟耗时计算"""
    time.sleep(0.5)
    return x ** 2

def demo_pool():
    print("\n" + "=" * 55)
    print("【2】Pool 进程池")
    print("=" * 55)

    cpu_count = multiprocessing.cpu_count()
    print(f"  当前 CPU 核心数: {cpu_count}")

    # --- map：最简单，类似内置 map()，阻塞直到全部完成 ---
    with multiprocessing.Pool(processes=4) as pool:  # with 语句自动 close+join
        results = pool.map(square, range(10))        # 把任务均匀分配给4个进程
        print(f"  pool.map 结果: {results}")

    # --- map vs apply vs starmap 对比 ---
    with multiprocessing.Pool(4) as pool:

        # map(func, iterable)：一个参数，最常用
        r1 = pool.map(square, [1, 2, 3, 4, 5])
        print(f"  map:     {r1}")

        # starmap(func, iterable)：多个参数，iterable 是元组列表
        # 等价于 [func(*args) for args in iterable]
        r2 = pool.starmap(pow, [(2,3),(3,2),(4,2)])  # pow(2,3), pow(3,2)...
        print(f"  starmap: {r2}")                    # [8, 9, 16]

        # apply(func, args)：单次调用，阻塞等待结果（较少用）
        r3 = pool.apply(square, (7,))
        print(f"  apply:   {r3}")

    # --- map_async / apply_async：异步版本，不阻塞主进程 ---
    with multiprocessing.Pool(4) as pool:
        # 提交任务后立刻返回 AsyncResult 对象，不阻塞
        async_result = pool.map_async(heavy_compute, range(8))
        print("  异步任务已提交，主进程继续做别的事...")
        time.sleep(0.1)
        results = async_result.get()    # get() 才阻塞，拿结果
        print(f"  异步结果: {results}")

    # Pool 核心方法速查：
    # pool.map(f, iterable)         → 同步，返回结果列表
    # pool.starmap(f, iterable)     → 同步，多参数版 map
    # pool.apply(f, args)           → 同步，单次调用
    # pool.map_async(f, iterable)   → 异步，返回 AsyncResult
    # pool.apply_async(f, args)     → 异步，单次调用
    # pool.close()                  → 不再接受新任务
    # pool.terminate()              → 立即终止所有进程
    # pool.join()                   → 等待所有进程完成（必须先 close）


# ============================================================
# 【3】Queue —— 进程间通信（生产者-消费者模型）
# ============================================================
# 进程内存独立，普通变量无法共享！
# multiprocessing.Queue 是进程安全的队列，底层用管道+锁实现
# 注意：不是 queue.Queue（那个是线程安全的，进程间不能用！）

def producer(q, items):
    """生产者：往队列里放数据"""
    for item in items:
        q.put(item)                     # 队列满时阻塞
        print(f"  生产: {item}")
        time.sleep(0.2)
    q.put(None)                         # 发送"毒丸"信号，通知消费者结束
    print("  生产者：发送结束信号")

def consumer(q):
    """消费者：从队列取数据"""
    while True:
        item = q.get()                  # 队列空时阻塞等待
        if item is None:                # 收到"毒丸"，退出
            print("  消费者：收到结束信号，退出")
            break
        print(f"  消费: {item} (处理中...)")
        time.sleep(0.3)

def demo_queue():
    print("\n" + "=" * 55)
    print("【3】Queue 进程间通信")
    print("=" * 55)

    q = multiprocessing.Queue(maxsize=5)   # maxsize=0 表示无限制

    p1 = multiprocessing.Process(target=producer, args=(q, [1,2,3,4,5]))
    p2 = multiprocessing.Process(target=consumer, args=(q,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Queue 方法速查：
    # q.put(item, block=True, timeout=None)  → 放入，满时阻塞
    # q.put_nowait(item)                     → 满时直接抛 Full 异常
    # q.get(block=True, timeout=None)        → 取出，空时阻塞
    # q.get_nowait()                         → 空时直接抛 Empty 异常
    # q.empty()                              → 是否为空（不可靠，仅参考）
    # q.qsize()                              → 当前元素数（不可靠，仅参考）


# ============================================================
# 【4】Pipe —— 管道通信（两个进程点对点）
# ============================================================
# Pipe() 返回两个 Connection 对象 (conn1, conn2)
# conn1.send() ↔ conn2.recv()，双向通信
# 比 Queue 更轻量，适合只有两个进程互相通信的场景
# Queue：多生产者多消费者；Pipe：一对一点对点

def pipe_sender(conn):
    """发送端"""
    data = [42, "hello", {"key": "value"}]  # 可以发送任意可 pickle 的对象
    for item in data:
        conn.send(item)
        print(f"  发送: {item}")
        time.sleep(0.2)
    conn.send(None)     # 结束信号
    conn.close()

def pipe_receiver(conn):
    """接收端"""
    while True:
        item = conn.recv()          # 阻塞等待数据
        if item is None:
            print("  接收端：管道关闭")
            break
        print(f"  接收: {item}")
    conn.close()

def demo_pipe():
    print("\n" + "=" * 55)
    print("【4】Pipe 管道通信")
    print("=" * 55)

    # duplex=True（默认）：双向管道，两端都能 send/recv
    # duplex=False：单向管道，conn1只能recv，conn2只能send
    parent_conn, child_conn = multiprocessing.Pipe(duplex=True)

    p1 = multiprocessing.Process(target=pipe_sender,   args=(parent_conn,))
    p2 = multiprocessing.Process(target=pipe_receiver, args=(child_conn,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Pipe 方法速查：
    # conn.send(obj)     → 发送任意可序列化对象
    # conn.recv()        → 接收，阻塞直到有数据
    # conn.send_bytes(b) → 发送字节串（更高效）
    # conn.recv_bytes()  → 接收字节串
    # conn.poll(timeout) → 检查是否有数据可读，不阻塞
    # conn.close()       → 关闭连接


# ============================================================
# 【5】综合实战：多进程并行计算 + Queue 汇总结果
# ============================================================
def compute_chunk(q, chunk):
    """计算一段数字的平方和，结果放入队列"""
    result = sum(x * x for x in chunk)
    q.put(result)
    print(f"  PID={os.getpid()} 计算 {chunk[0]}~{chunk[-1]} 完成，结果={result}")

def demo_combined():
    print("\n" + "=" * 55)
    print("【5】综合实战：并行计算平方和")
    print("=" * 55)

    # 把 0~999 分成 4 段，4个进程并行计算，Queue 汇总
    data = list(range(1000))
    chunks = [data[i::4] for i in range(4)]     # 按步长切分：[0,4,8,...], [1,5,9,...]...

    q = multiprocessing.Queue()
    processes = [
        multiprocessing.Process(target=compute_chunk, args=(q, chunk))
        for chunk in chunks
    ]

    for p in processes: p.start()
    for p in processes: p.join()

    # 从队列里取出所有结果并汇总
    total = 0
    while not q.empty():
        total += q.get()

    print(f"\n  并行计算总平方和: {total}")
    print(f"  验证（单进程）:   {sum(x*x for x in range(1000))}")


# ============================================================
# Windows 必须在 main 保护下运行，Linux/Mac 可直接运行
# ============================================================
if __name__ == "__main__":
    demo_process()
    demo_pool()
    demo_queue()
    demo_pipe()
    demo_combined()