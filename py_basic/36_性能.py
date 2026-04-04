"""
【Python 性能优化：timeit、cProfile、lru_cache 与 slots】
请在 VS Code 中运行，直观感受性能分析与优化的震撼！
"""
import timeit
import cProfile
import pstats
import sys
from functools import lru_cache

print("="*10, "1. timeit：微观性能裁判", "="*10)
# a=1: 比较“字符串拼接”的两种写法
# 很多新手喜欢用 + 号拼接字符串，大厂规范要求必须用 .join()。到底差多少？
setup_code = "words = ['AI', 'Python', 'Performance'] * 100"
test_plus = "s = '';\nfor w in words: s += w"
test_join = "s = ''.join(words)"

# timeit 自动关闭了垃圾回收，并执行 10000 次取总时间，极其精准
time_plus = timeit.timeit(stmt=test_plus, setup=setup_code, number=10000)
time_join = timeit.timeit(stmt=test_join, setup=setup_code, number=10000)

print(f"[+号拼接] 耗时: {time_plus:.4f} 秒")
print(f"[join拼接] 耗时: {time_join:.4f} 秒 (通常快数倍！)")


print("\n"+"="*10, "2. lru_cache：算法刷题的作弊级魔法", "="*10)
# a=2: 算法题经典场景：递归爆炸
# 不加缓存的斐波那契，n=35 就要算好几秒，因为存在海量重复计算（指数级复杂度 O(2^N)）
def slow_fib(n):
    if n < 2: return n
    return slow_fib(n-1) + slow_fib(n-2)

# 加上 @lru_cache 后，自动应用备忘录模式（记忆化搜索），时间复杂度瞬间降为 O(N)！
@lru_cache(maxsize=None)
def fast_fib(n):
    if n < 2: return n
    return fast_fib(n-1) + fast_fib(n-2)

print("正在计算 slow_fib(35) ... (请耐心等待1~2秒)")
print(f"未使用缓存结果: {slow_fib(35)}")
print("正在计算 fast_fib(100) ... (瞬间出结果！)")
print(f"使用缓存结果: {fast_fib(100)}")
print(f"缓存命中统计: {fast_fib.cache_info()}") # 还能查看缓存命中率！


print("\n"+"="*10, "3. __slots__：海量对象的内存瘦身", "="*10)
# a=3: 当我们需要实例化几百万个 AI 训练数据节点时
class NormalNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class SlottedNode:
    # 缝死口袋：彻底废除底层的动态 __dict__
    __slots__ = ['val', 'left', 'right']
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

node1 = NormalNode(10)
node2 = SlottedNode(10)

# sys.getsizeof 只能测量对象外壳，NormalNode 真正吃内存的是隐藏的 __dict__！
dict_size = sys.getsizeof(node1.__dict__) 
print(f"普通节点附带的隐藏字典大小: {dict_size} bytes")
try:
    print(node2.__dict__)
except AttributeError:
    print(f"Slotted 节点根本没有 __dict__，省下了这笔巨大的开销！")


print("\n"+"="*10, "4. cProfile：系统级性能 X 光机", "="*10)
# a=4: 模拟一个复杂的 AI 处理流程，找出瓶颈在哪
def clean_data():
    # 模拟快速操作
    return [i for i in range(100000)]

def train_model():
    # 模拟耗时操作 (乘法计算)
    return [i * i for i in range(100000)]

def main_pipeline():
    clean_data()
    train_model()

print("\n正在生成体检报告单...")
# 生成分析器并运行主函数
profiler = cProfile.Profile()
profiler.enable()
main_pipeline()
profiler.disable()

# 格式化输出体检报告 (按累计耗时 cumulative 降序排列)
stats = pstats.Stats(profiler).sort_stats('cumulative')
# 只打印前 10 行最重要的信息
stats.print_stats(10)