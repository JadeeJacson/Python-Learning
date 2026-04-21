# ============================================================
# Python 多线程完全指南
# threading / Thread / Lock / RLock / Semaphore / Event / GIL
# ============================================================

import threading
import time
import random

# ============================================================
# 【核心概念】GIL —— 全局解释器锁
# ============================================================
# GIL (Global Interpreter Lock)：CPython 解释器的一把"全局锁"
# 同一时刻，只允许一个线程执行 Python 字节码。
#
# 结论（非常重要！）：
#   ✅ I/O 密集型任务（网络请求、文件读写）→ 多线程有效，线程在等待 I/O 时会释放 GIL
#   ❌ CPU 密集型任务（大量计算）         → 多线程几乎无加速，用 multiprocessing 替代
#
# 你可以把 GIL 想象成一个"轮流使用计算器"的规定：
# 多个线程只能排队用，不能同时算。但"等外卖"的线程不占计算器，所以 I/O 场景有效。

print("=" * 55)
print("【1】threading.Thread 基本用法")
print("=" * 55)

# --- Thread 两种创建方式 ---

# 方式一：直接传入函数（最常用）
def download(name, duration):
    print(f"  [{name}] 开始下载...")
    time.sleep(duration)          # 模拟 I/O 等待，此时线程释放 GIL
    print(f"  [{name}] 下载完成！耗时 {duration}s")

t1 = threading.Thread(target=download, args=("文件A", 2))
t2 = threading.Thread(target=download, args=("文件B", 1))

t1.start()   # 启动线程（非阻塞，主线程继续往下走）
t2.start()

t1.join()    # 阻塞主线程，等 t1 结束
t2.join()    # 阻塞主线程，等 t2 结束
# 两个任务"并发"执行，总耗时约 2s 而非 3s ← I/O 密集型多线程的价值


# 方式二：继承 Thread 类（逻辑复杂时更清晰）
class DownloadThread(threading.Thread):
    def __init__(self, name, duration):
        super().__init__()
        self.name = name
        self.duration = duration

    def run(self):          # 必须重写 run()，不要直接调用 run()，要调用 start()
        print(f"  [{self.name}] 子类线程启动")
        time.sleep(self.duration)
        print(f"  [{self.name}] 子类线程结束")

t3 = DownloadThread("文件C", 1)
t3.start()
t3.join()

# --- 常用属性/方法速查 ---
# thread.start()            # 启动线程
# thread.join(timeout=None) # 等待线程结束，timeout 单位秒
# thread.is_alive()         # 线程是否还在运行 → True/False
# thread.daemon = True      # 设为守护线程：主线程结束时该线程自动销毁（放在 start() 之前设置）
# threading.current_thread()# 返回当前线程对象
# threading.enumerate()     # 返回所有存活线程列表


print("\n" + "=" * 55)
print("【2】Lock —— 互斥锁（最常用的同步原语）")
print("=" * 55)

# 问题场景：多线程同时修改共享变量 → 数据竞争（Race Condition）
counter = 0

def unsafe_increment():
    global counter
    for _ in range(100000):
        counter += 1   # ← 非原子操作！底层是 读-加-写 三步，线程可能在中间被切换

threads = [threading.Thread(target=unsafe_increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"  不加锁结果（应为500000，实际）: {counter}")  # 大概率 < 500000，说明数据丢失！

# 解决方案：Lock
counter = 0
lock = threading.Lock()         # 创建一把锁，全局共享同一个 lock 对象

def safe_increment():
    global counter
    for _ in range(100000):
        lock.acquire()          # 加锁：若锁已被占用则阻塞等待
        counter += 1            # 临界区：同一时刻只有一个线程能进入
        lock.release()          # 释放锁

# 更推荐：用 with 语句，自动 acquire/release，即使异常也不会死锁
def safe_increment_with():
    global counter
    for _ in range(100000):
        with lock:              # ← 等价于 acquire + try/finally release
            counter += 1

threads = [threading.Thread(target=safe_increment_with) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"  加锁结果（应为500000，实际）: {counter}")   # 一定是 500000 ✅


print("\n" + "=" * 55)
print("【3】RLock —— 可重入锁")
print("=" * 55)

# 问题：普通 Lock 不可重入，同一线程连续 acquire 两次会死锁！
# RLock（Reentrant Lock）：同一线程可以多次 acquire，每次 acquire 对应一次 release

rlock = threading.RLock()

def recursive_task(n):
    with rlock:                 # 第一次加锁
        if n <= 0:
            return
        print(f"  recursive_task({n})")
        with rlock:             # 同一线程再次加锁 → RLock 允许，Lock 会死锁！
            recursive_task(n - 1)

t = threading.Thread(target=recursive_task, args=(3,))
t.start()
t.join()
# 使用场景：递归函数、同一线程内调用多个都需要加锁的方法（如父方法调子方法）


print("\n" + "=" * 55)
print("【4】Semaphore —— 信号量（控制并发数量）")
print("=" * 55)

# Semaphore 内部维护一个计数器，acquire() -1，release() +1
# 计数器为 0 时，acquire() 阻塞 → 用于限制同时访问资源的线程数
# 场景：连接池、爬虫限速（最多同时 3 个请求）

sem = threading.Semaphore(3)    # 最多允许 3 个线程同时执行

def fetch_url(url_id):
    with sem:                   # 超过 3 个线程时，第 4 个在这里阻塞
        print(f"  正在请求 URL-{url_id}（当前并发受限于3）")
        time.sleep(1)           # 模拟网络请求
        print(f"  URL-{url_id} 请求完成")

threads = [threading.Thread(target=fetch_url, args=(i,)) for i in range(7)]
for t in threads: t.start()
for t in threads: t.join()
# 观察输出：每批最多 3 个同时打印"正在请求"


print("\n" + "=" * 55)
print("【5】Event —— 线程间通信/信号通知")
print("=" * 55)

# Event 内部维护一个布尔标志（默认 False）
# event.wait()   → 阻塞直到标志变为 True
# event.set()    → 将标志设为 True，唤醒所有 wait() 的线程
# event.clear()  → 将标志重置为 False
# event.is_set() → 返回当前标志值

# 场景：生产者就绪后通知消费者开始工作
event = threading.Event()

def consumer():
    print("  消费者：等待数据就绪...")
    event.wait()                # 阻塞，直到 event.set() 被调用
    print("  消费者：收到信号，开始处理数据！")

def producer():
    print("  生产者：准备数据中...")
    time.sleep(2)
    print("  生产者：数据已就绪，发出信号")
    event.set()                 # 唤醒所有在 wait() 的线程

t_consumer = threading.Thread(target=consumer)
t_producer = threading.Thread(target=producer)
t_consumer.start()
t_producer.start()
t_consumer.join()
t_producer.join()


print("\n" + "=" * 55)
print("【6】综合实战：多线程爬虫模拟（I/O 密集型）")
print("=" * 55)

# 模拟：限速爬取 10 个 URL，最多 3 个并发，全部完成后汇总结果
results = []
results_lock = threading.Lock()
semaphore = threading.Semaphore(3)

def crawl(url_id):
    with semaphore:
        delay = random.uniform(0.5, 1.5)
        time.sleep(delay)                       # 模拟网络延迟
        data = f"page_{url_id}_content"
        with results_lock:                      # 写共享列表需要加锁
            results.append(data)
        print(f"  ✅ URL-{url_id} 爬取完成")

start = time.time()
threads = [threading.Thread(target=crawl, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print(f"\n  共爬取 {len(results)} 个页面，耗时 {time.time()-start:.2f}s")
print(f"  结果预览: {results[:3]}")