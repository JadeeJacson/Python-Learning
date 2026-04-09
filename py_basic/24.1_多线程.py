"""
【Python 多线程兵法：GIL 下的 I/O 破局之道】
请在 VS Code 中运行。仔细观察打印的顺序，体会“并发”的魔力与“锁”的秩序。
"""
import threading
import time
import random

print("="*10, "大厂业务场景：高并发 AI 语料爬取与处理", "="*10)

# 1. 兵器库初始化
total_downloaded = 0                 # 共享的全局变量（极度危险，必须加锁）
data_lock = threading.Lock()         # 互斥锁：保护 total_downloaded 不被写乱
api_limiter = threading.Semaphore(3) # 信号量：限制并发，最多同时允许 3 个线程下载
start_gun = threading.Event()        # 事件发令枪：让所有线程就位后一起开始

def worker_thread(worker_id):
    """打工人的标准作业流"""
    print(f"👷 [打工人 {worker_id}] 已就位，等待发令枪...")
    
    # a=1: Event 阻塞。所有线程卡在这里，直到主线程 set()
    start_gun.wait() 
    
    # a=2: Semaphore 限制。去保安那里领令牌，最多3人同时执行
    with api_limiter:
        print(f"   🚀 [打工人 {worker_id}] 拿到令牌，开始下载语料...")
        # 模拟 I/O 密集型耗时操作 (此时 GIL 会被主动释放，其他线程可以趁机运行！)
        time.sleep(random.uniform(0.5, 1.5)) 
        print(f"   ✅ [打工人 {worker_id}] 下载完毕！准备写入全局数据库。")
        
        # a=3: Lock 保护。开始修改共享变量了，必须拿唯一钥匙！
        # 如果不用 with 语法，你需要手动 data_lock.acquire() 和 data_lock.release()
        with data_lock:
            global total_downloaded
            # 这里的读写操作如果不加锁，极易发生覆盖！
            local_copy = total_downloaded
            # 假装这里有一些轻量级的 CPU 计算
            local_copy += 1 
            total_downloaded = local_copy
            print(f"      🔒 [打工人 {worker_id}] 修改了总数: {total_downloaded}")

# 2. 招募 5 个打工人 (创建线程)
threads = []
for i in range(1, 6):
    # target 指定要跑的函数，args 给函数传参 (注意必须是个元组，哪怕只有一个元素也要加逗号)
    t = threading.Thread(target=worker_thread, args=(i,))
    threads.append(t)
    t.start() # start() 只是启动线程，但线程内部目前卡在了 start_gun.wait()

print("\n👑 [主线程] 老板巡视一圈，确认大家都准备好了。")
time.sleep(1) # 假装老板喝了口茶
print("👑 [主线程] 砰！发令枪响，开始干活！\n")

# a=4: Event 触发！所有等待的线程瞬间苏醒被放行
start_gun.set()

# a=5: 极其关键的一步！主线程必须等待所有子线程干完活，再往下走
for t in threads:
    t.join() 

print(f"\n🎉 [主线程] 所有打工人下班！最终采集到的语料总数: {total_downloaded}")