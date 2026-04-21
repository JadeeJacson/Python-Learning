# ==============================================================================
# 【核心概念讲解 & 底层逻辑：费曼技巧讲透多线程与GIL】
# ==============================================================================
# 1. 什么是多线程 (Thread)？
#    【费曼讲解】：想象你是一个包工头，你的程序是一个工地。单线程就是只有1个工人在干活；
#    多线程就是你雇了多个工人（Thread）同时干活。他们共享同一个工地（内存空间）。
# 
# 2. 为什么需要锁 (Lock / RLock)？
#    【费曼讲解】：多个工人共用一个洗手间（共享变量），如果不排队（加锁），就会冲进去打架（数据错乱，竞态条件）。
#    Lock就是洗手间门上的一把锁。RLock（可重入锁）是高级锁，同一个工人可以带着这把钥匙多次进出多个相连的门，不会把自己锁死。
# 
# 3. 什么是信号量 (Semaphore)？
#    【费曼讲解】：工地只有3个免费停车位。Semaphore(3) 就是保安，只允许3辆车同时进来，后面的车得等前面的开走。
#    常用于控制并发数量（如数据库连接池、限流）。
# 
# 4. 什么是事件 (Event)？
#    【费曼讲解】：包工头手里的红绿灯。红灯时所有工人原地等待（event.wait()），
#    绿灯亮起（event.set()），所有工人立刻一起开始干活。用于线程间的协调通信。
# 
# 5. 终极Boss：GIL (Global Interpreter Lock 全局解释器锁)
#    【底层逻辑】：Python解释器（CPython）里有个霸道的规定：
#    "同一时刻，即使你有100个CPU核心，也只能有1个线程在执行Python字节码！"
#    【结论】：Python的多线程是“伪并行”。
#    - 对于CPU密集型（死算代码，如大量加减乘除）：多线程不仅没用，反而因为频繁切换线程，比单线程还慢！
#    - 对于I/O密集型（网络请求、读写文件、爬虫）：多线程有奇效！因为一个工人等网络下载时，会自动交出执行权，其他工人可以趁机干活。

import threading
import time
import random

# ==============================================================================
# 【可运行的实战代码：模拟多线程经典场景】
# ==============================================================================

# 全局共享变量
shared_counter = 0

# 1. Lock: 保护共享变量
counter_lock = threading.Lock() # 基础锁

def worker_add(worker_id):
    global shared_counter
    # 模拟干点别的事 (I/O操作会释放GIL)
    time.sleep(random.uniform(0.01, 0.05)) 
    
    # 【常见用法】：使用 with 语句自动获取和释放锁，防止忘记释放导致死锁
    with counter_lock:
        # 进入临界区，此时只有一个线程能执行以下代码
        temp = shared_counter
        temp += 1
        shared_counter = temp
        print(f"工人 {worker_id} 将计数器加到了 {shared_counter}")

# 2. Semaphore: 控制并发数量 (如限制最多2个线程同时下载)
pool_sema = threading.Semaphore(2)

def worker_download(worker_id):
    with pool_sema: # 保安：最多进2个
        print(f"[下载任务] {worker_id} 开始下载...")
        time.sleep(0.1) # 模拟下载耗时
        print(f"[下载任务] {worker_id} 下载完成！")

# 3. Event: 线程协调 (如主线程准备好数据后，通知工作线程开工)
start_event = threading.Event()

def worker_wait_for_signal(worker_id):
    print(f"(等待者 {worker_id}) 就绪，等待发令枪...")
    start_event.wait() # 阻塞在这里，等待红灯变绿灯
    print(f"(等待者 {worker_id}) 听到枪声，冲啊！")

if __name__ == "__main__":
    print("--- 场景1：Lock 保护共享数据 ---")
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_add, args=(i,)) # 创建线程
        threads.append(t)
        t.start() # 启动线程
    
    for t in threads:
        t.join() # 【关键方法】：主线程阻塞，等待子线程t执行完毕再往下走
    print(f"最终计数器结果: {shared_counter} (预期为5)\n")

    print("--- 场景2：Semaphore 限制并发 ---")
    dl_threads = []
    for i in range(5):
        t = threading.Thread(target=worker_download, args=(f"文件{i}",))
        dl_threads.append(t)
        t.start()
    for t in dl_threads: t.join()
    print()

    print("--- 场景3：Event 统一发令 ---")
    runner_threads = []
    for i in range(3):
        t = threading.Thread(target=worker_wait_for_signal, args=(i,))
        runner_threads.append(t)
        t.start()
    
    print("[主线程] 裁判正在检查跑道...")
    time.sleep(0.5)
    print("[主线程] 砰！(发令枪响)")
    start_event.set() # 【关键方法】：绿灯亮起，唤醒所有wait的线程
    # 注意：event.clear() 可以重新把绿灯变回红灯

    for t in runner_threads: t.join()
    print("\n所有演示执行完毕！")