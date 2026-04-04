"""
【Python 生成器进阶：send、throw、close (双向通信)】
请在 VS Code 中运行。重点在 running_average_coroutine 内部打断点，
观察 yield 语句是如何接收外部传进来的 new_value 的！
"""

print("="*10, "1. send()：给暂停的生成器喂数据", "="*10)
# a=1: 实战场景：我们需要实时计算 AI 训练过程中的 Loss 移动平均值。
# 每次外部算出一个新 Loss，就塞给生成器，它立刻返回当前的平均值。

def running_average_coroutine():
    """这是一个能接收外部数据的生成器（协程）"""
    total = 0.0
    count = 0
    average = None
    
    while True:
        # ⚠️ 究极核心代码：x = yield y
        # 1. 它是从右往左执行的！先向外吐出 y (也就是 average)，然后瞬间冻结。
        # 2. 当外部调用 send(10) 唤醒它时，收到的 10 会赋值给左边的 x (也就是 new_value)。
        try:
            new_value = yield average
        except ValueError:
            # 这里的 except 是为后面的 throw() 准备的
            print("  [内部] 收到报错：忽略这条坏数据！")
            continue 
            
        print(f"  [内部] 工人苏醒，收到了外部传来的数据: {new_value}")
        total += new_value
        count += 1
        average = total / count

# 实例化生成器
avg_calculator = running_average_coroutine()

# 💣 致命陷阱：预激（Priming）生成器
# 刚造出来的工人还没有走到第一个 yield，你不能直接塞数据！
# 必须先用 next() 或 send(None) 让他走到第一个 yield 停下来，准备好接数据。
next(avg_calculator) 
print("[外部] 预激完成，工人已在工作台就位。\n")

print(f"[外部] 塞入 Loss=10.0，当前平均: {avg_calculator.send(10.0)}")
print(f"[外部] 塞入 Loss=20.0，当前平均: {avg_calculator.send(20.0)}")


print("\n"+"="*10, "2. throw()：往生成器里扔炸弹", "="*10)
# a=2: 假设外部发现数据采集器出错了，收到了一条坏数据。
# 我们不想塞入脏数据，而是向生成器抛出一个 ValueError 异常。

print("[外部] 发现脏数据，向内部抛出 ValueError 炸弹！")
# 生成器会在上一层暂停的 yield 处引发 ValueError，
# 因为内部写了 try...except，所以工人捕获了炸弹，打印了忽略提示，
# 并且立刻进入下一次循环，在新的 yield 处再次暂停，返回当前的 average (依然是 15.0)
current_avg = avg_calculator.throw(ValueError)
print(f"[外部] 炸弹抛出后，工人存活，返回平均: {current_avg}\n")


print("="*10, "3. close()：强行关闭生成器", "="*10)
# a=3: 训练结束，打扫战场，让工人下班。

print("[外部] 训练结束，调用 close() 关闭生成器。")
# 调用 close() 会在生成器内部暂停的 yield 处引发一个 GeneratorExit 异常。
# 这个异常如果不捕获，生成器就会默默地优雅退出。
avg_calculator.close()

# 试图在一个已经 close 的生成器上继续 send，会引发 StopIteration 报错
try:
    avg_calculator.send(30.0)
except StopIteration:
    print("[外部] 报错：StopIteration，因为工人已经下班回家了！")