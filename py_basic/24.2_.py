# ============================================================
# Python 并发编程：多线程
# threading / Thread / Lock / RLock / Semaphore / Event / GIL
# ============================================================
# 前置理解：
#   进程 = 一个独立运行的程序（有独立内存空间）
#   线程 = 进程内的执行单元，同一进程的线程共享内存
#   并发 = 多个任务交替执行（单核也能做）
#   并行 = 多个任务真正同时执行（需要多核）
# ============================================================


# ────────────────────────────────────────────────────────────
# 第一块：GIL —— 理解 Python 多线程的核心限制
# GIL = Global Interpreter Lock（全局解释器锁）
# 本质：CPython 解释器同一时刻只允许一个线程执行 Python 字节码
# 类比：一个厨房只有一把菜刀（GIL），多个厨师（线程）必须轮流用
# ────────────────────────────────────────────────────────────

print("=== GIL 的影响：CPU密集型 vs IO密集型 ===")

import threading
import time

# ── CPU密集型：多线程不会提速，反而因切换开销更慢 ──
def cpu_task(n):
    """纯计算任务，一直占用 CPU"""
    count = 0
    while count < n:
        count += 1

start = time.time()
cpu_task(50_000_000)          # 单线程
print(f"单线程 CPU任务: {time.time() - start:.2f}s")

start = time.time()
t1 = threading.Thread(target=cpu_task, args=(25_000_000,))
t2 = threading.Thread(target=cpu_task, args=(25_000_000,))
t1.start(); t2.start()
t1.join();  t2.join()
print(f"双线程 CPU任务: {time.time() - start:.2f}s")
# 结论：双线程不比单线程快，甚至更慢（GIL 导致）

# ── IO密集型：线程等待IO时会释放 GIL，多线程有效提速 ──
def io_task(name, seconds):
    """模拟 IO 等待（网络请求、文件读写）"""
    time.sleep(seconds)   # sleep 会释放 GIL，其他线程可以运行

start = time.time()
io_task("A", 1); io_task("B", 1)   # 串行：2秒
print(f"串行 IO任务: {time.time() - start:.2f}s")

start = time.time()
t1 = threading.Thread(target=io_task, args=("A", 1))
t2 = threading.Thread(target=io_task, args=("B", 1))
t1.start(); t2.start()
t1.join();  t2.join()              # 并发：约1秒
print(f"并发 IO任务: {time.time() - start:.2f}s")
# 结论：IO密集型用多线程，CPU密集型用多进程（multiprocessing）


# ────────────────────────────────────────────────────────────
# 第二块：Thread —— 创建和管理线程
# ────────────────────────────────────────────────────────────

print("\n=== Thread：两种创建方式 ===")

# ── 方式1：传入函数（最常用）──
def worker(name, delay):
    time.sleep(delay)
    print(f"[{name}] 完成，延迟={delay}s")

t1 = threading.Thread(target=worker, args=("线程A", 0.1))
t2 = threading.Thread(target=worker, args=("线程B", 0.2), daemon=True)
# daemon=True：守护线程，主线程结束时自动销毁（不会阻塞程序退出）
# daemon=False（默认）：主线程会等待其执行完毕

t1.start()   # 启动线程（非阻塞，立即返回）
t2.start()

t1.join()    # 主线程在此阻塞，等待 t1 执行完
t2.join()    # 等待 t2 执行完
print("所有线程执行完毕")


# ── 方式2：继承 Thread 类（适合需要封装状态的场景）──
class DownloadThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.result = None        # 用实例变量保存执行结果

    def run(self):                # 重写 run()，线程启动时执行此方法
        time.sleep(0.1)           # 模拟下载
        self.result = f"下载完成: {self.url}"

dt = DownloadThread("https://example.com/data.csv")
dt.start()
dt.join()
print(dt.result)   # 通过实例属性获取结果


# ────────────────────────────────────────────────────────────
# 第三块：Lock —— 互斥锁，解决竞态条件
# 问题：多线程共享变量时，"读-改-写"不是原子操作，会出错
# ────────────────────────────────────────────────────────────

print("\n=== Lock：没有锁的竞态条件 ===")

counter = 0

def unsafe_increment():
    global counter
    for _ in range(100_000):
        counter += 1   # 非原子操作：读取→加1→写回，三步之间可能被打断

threads = [threading.Thread(target=unsafe_increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"预期: 500000，实际: {counter}")   # 实际结果小于500000（有数据丢失）


print("\n=== Lock：加锁保证原子性 ===")

counter = 0
lock = threading.Lock()   # 创建一把锁

def safe_increment():
    global counter
    for _ in range(100_000):
        with lock:         # with 语句自动 acquire() 和 release()
            counter += 1   # 同一时刻只有一个线程能执行这里

threads = [threading.Thread(target=safe_increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"预期: 500000，实际: {counter}")   # 输出: 500000 ✓


# ────────────────────────────────────────────────────────────
# 第四块：RLock —— 可重入锁
# 问题：同一线程对 Lock 加锁两次会死锁
# RLock：同一线程可以多次 acquire()，内部计数，全部 release() 后才真正解锁
# 场景：递归函数或互相调用的方法都需要加锁时
# ────────────────────────────────────────────────────────────

print("\n=== RLock vs Lock：可重入对比 ===")

# Lock 死锁演示（注释掉，避免程序卡住）
# lock = threading.Lock()
# with lock:
#     with lock:   # 同一线程第二次 acquire，永远等待自己释放 → 死锁！
#         pass

rlock = threading.RLock()   # 可重入锁

def recursive_task(n):
    with rlock:              # 同一线程可以多次进入
        if n <= 0:
            return
        print(f"层级 {n}")
        recursive_task(n - 1)   # 递归中再次 acquire rlock，不会死锁

recursive_task(3)


# ────────────────────────────────────────────────────────────
# 第五块：Semaphore —— 信号量，控制并发数量
# 本质：内部维护一个计数器，acquire() -1，release() +1
#       计数器为0时，新的 acquire() 会阻塞等待
# 场景：限制同时访问数据库/API 的线程数（连接池）
# ────────────────────────────────────────────────────────────

print("\n=== Semaphore：限制并发数为3 ===")

# 模拟：10个线程同时发请求，但最多3个线程同时访问"数据库"
semaphore = threading.Semaphore(3)   # 最多允许3个线程同时进入

def db_query(thread_id):
    with semaphore:    # 计数>0才能进入，否则阻塞
        print(f"线程{thread_id:02d} 开始查询DB")
        time.sleep(0.2)
        print(f"线程{thread_id:02d} 完成查询")

threads = [threading.Thread(target=db_query, args=(i,)) for i in range(8)]
start = time.time()
for t in threads: t.start()
for t in threads: t.join()
print(f"总耗时: {time.time()-start:.2f}s（无限制约需0.2s，限3并发约需0.6s）")


# ────────────────────────────────────────────────────────────
# 第六块：Event —— 线程间通信，等待某个"信号"
# 本质：内部维护一个布尔标志
#   event.wait()  → 阻塞直到标志为 True
#   event.set()   → 将标志设为 True，唤醒所有等待的线程
#   event.clear() → 将标志重置为 False
# 场景：生产者-消费者，主线程通知子线程开始工作
# ────────────────────────────────────────────────────────────

print("\n=== Event：生产者-消费者通信 ===")

data_ready = threading.Event()   # 初始标志为 False
shared_data = []

def producer():
    print("[生产者] 正在准备数据...")
    time.sleep(0.3)
    shared_data.append([1, 2, 3, 4, 5])
    print("[生产者] 数据准备完毕，发出信号")
    data_ready.set()             # 标志置为 True，唤醒消费者

def consumer():
    print("[消费者] 等待数据...")
    data_ready.wait()            # 阻塞直到 set() 被调用
    print(f"[消费者] 收到数据: {shared_data[0]}")

t_prod = threading.Thread(target=producer)
t_cons = threading.Thread(target=consumer)
t_cons.start()   # 消费者先启动，进入等待
t_prod.start()   # 生产者后启动，准备好后发信号
t_prod.join()
t_cons.join()


# ────────────────────────────────────────────────────────────
# 综合实战：多线程爬虫（IO密集型的典型应用）
# 模拟：批量下载URL，限制最大并发数，收集结果
# ────────────────────────────────────────────────────────────

print("\n=== 综合实战：并发下载器 ===")

import random

def fetch_url(url, results, lock, semaphore):
    with semaphore:                        # 限制最大并发数
        delay = random.uniform(0.1, 0.4)  # 模拟网络延迟
        time.sleep(delay)
        result = f"{url} → {int(delay*1000)}ms"
        with lock:                         # 写入共享列表时加锁
            results.append(result)

urls = [f"https://api.example.com/item/{i}" for i in range(10)]
results = []
lock = threading.Lock()
semaphore = threading.Semaphore(4)   # 最多4个并发

start = time.time()
threads = [
    threading.Thread(target=fetch_url, args=(url, results, lock, semaphore))
    for url in urls
]
for t in threads: t.start()
for t in threads: t.join()

print(f"下载完成 {len(results)}/10 个URL，总耗时: {time.time()-start:.2f}s")
for r in sorted(results):
    print(f"  {r}")