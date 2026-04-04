# ============================================================
# 标准库第一弹：collections / itertools / functools / math / random
# 场景：算法刷题高频工具
# ============================================================
import collections
import itertools
import functools
import math
import random


# ══════════════════════════════════════════════════════════════
# 一、collections —— 比内置容器更强的数据结构
# ══════════════════════════════════════════════════════════════

# ── 1. Counter：计数器，词频/字符频率统计首选 ──────────────
print("── Counter ──")

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
cnt = collections.Counter(words)
print(cnt)                        # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(cnt["apple"])               # 3
print(cnt["不存在的key"])          # 0  ⬅ 不会 KeyError，直接返回 0

# 算法题常用：TopK 高频元素
print(cnt.most_common(2))         # [('apple', 3), ('banana', 2)]

# 两个 Counter 可以直接相加/相减
cnt2 = collections.Counter(["banana", "cherry", "cherry"])
print(cnt + cnt2)                 # 合并计数
print(cnt - cnt2)                 # 差集（只保留正数）


# ── 2. defaultdict：带默认值的字典，告别 KeyError ──────────
print("\n── defaultdict ──")

# 普通 dict 访问不存在的 key 会 KeyError
# defaultdict 会自动用你指定的工厂函数创建默认值

graph = collections.defaultdict(list)   # 默认值是空 list
graph[0].append(1)   # key=0 不存在时自动创建 []，再 append
graph[0].append(2)
graph[1].append(3)
print(dict(graph))   # {0: [1, 2], 1: [3]}  ← 建图的标准写法

# 其他常用工厂：int（默认0）、set（默认空set）
freq = collections.defaultdict(int)
for c in "abracadabra":
    freq[c] += 1     # 不用判断 key 存不存在
print(dict(freq))


# ── 3. deque：双端队列，BFS 标配 ──────────────────────────
print("\n── deque ──")

dq = collections.deque([1, 2, 3])
dq.appendleft(0)     # 左端插入 O(1)  ⬅ list.insert(0,x) 是 O(n)，别用！
dq.append(4)         # 右端插入 O(1)
print(dq)            # deque([0, 1, 2, 3, 4])
print(dq.popleft())  # 0，左端弹出 O(1)
print(dq.pop())      # 4，右端弹出 O(1)

# BFS 模板：
# queue = deque([start])
# while queue:
#     node = queue.popleft()
#     for neighbor in graph[node]:
#         queue.append(neighbor)

# maxlen：固定长度窗口，自动丢弃溢出元素（滑动窗口题很好用）
window = collections.deque(maxlen=3)
for x in range(6):
    window.append(x)
    print(list(window))   # 始终只保留最近3个


# ── 4. OrderedDict：有序字典（LRU Cache 手写必用）─────────
print("\n── OrderedDict ──")

od = collections.OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3
od.move_to_end("a")          # 把 "a" 移到末尾
print(list(od.keys()))       # ['b', 'c', 'a']
od.move_to_end("c", last=False)  # 移到开头
print(list(od.keys()))       # ['c', 'b', 'a']


# ══════════════════════════════════════════════════════════════
# 二、itertools —— 惰性迭代工具，处理组合/排列/分组
# ══════════════════════════════════════════════════════════════
print("\n── itertools ──")

# accumulate：前缀和（算法题高频）
nums = [1, 2, 3, 4, 5]
prefix = list(itertools.accumulate(nums))
print(prefix)          # [1, 3, 6, 10, 15]

# 前缀积、前缀最大值
import operator
print(list(itertools.accumulate(nums, operator.mul)))  # [1,2,6,24,120]
print(list(itertools.accumulate(nums, max)))            # [1,2,3,4,5]

# combinations / permutations：组合/排列（回溯题对比用）
print(list(itertools.combinations([1,2,3], 2)))   # [(1,2),(1,3),(2,3)]
print(list(itertools.permutations([1,2,3], 2)))   # [(1,2),(1,3),(2,1)...]

# chain：把多个可迭代对象串成一个，不创建新列表
a, b = [1, 2], [3, 4]
print(list(itertools.chain(a, b)))   # [1, 2, 3, 4]  比 a+b 省内存

# product：笛卡尔积（多层 for 循环的替代）
print(list(itertools.product([0,1], repeat=2)))  # [(0,0),(0,1),(1,0),(1,1)]


# ══════════════════════════════════════════════════════════════
# 三、functools —— 函数工具
# ══════════════════════════════════════════════════════════════
print("\n── functools ──")

# lru_cache：记忆化搜索，递归题加速核武器
@functools.lru_cache(maxsize=None)   # maxsize=None 表示无限缓存
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(50))          # 瞬间出结果，没有 cache 会指数级爆炸
print(fib.cache_info()) # 查看命中情况

# ⚠️ lru_cache 要求参数必须可哈希（不能传 list/dict）
# 传列表时先转成 tuple：fib(tuple(arr))

# reduce：累计计算（理解函数式编程用）
print(functools.reduce(lambda acc, x: acc * x, [1,2,3,4]))  # 24，连乘


# ══════════════════════════════════════════════════════════════
# 四、math / random
# ══════════════════════════════════════════════════════════════
print("\n── math / random ──")

print(math.gcd(12, 8))          # 4，最大公约数（算法题常用）
print(math.lcm(4, 6))           # 12，最小公倍数（Python 3.9+）
print(math.inf)                 # 正无穷，初始化 min 值用
print(math.log2(1024))          # 10.0
print(math.isqrt(17))           # 4，整数平方根，比 int(sqrt()) 更精确

random.seed(42)                 # 固定随机种子，结果可复现（调试必用）
print(random.randint(1, 10))    # [1,10] 闭区间随机整数
arr = [1, 2, 3, 4, 5]
random.shuffle(arr)             # 原地打乱
print(arr)
print(random.sample(arr, 3))    # 不放回抽样，返回新列表
print(random.choice(arr))       # 随机取一个元素





# ============================================================
# 标准库第二弹：os / sys / pathlib / json / re / time / datetime
# 场景：实习工程开发日常操作
# ============================================================
import os
import sys
import json
import re
import time
import datetime
from pathlib import Path


# ══════════════════════════════════════════════════════════════
# 一、os —— 和操作系统打交道
# ══════════════════════════════════════════════════════════════
print("── os ──")

print(os.getcwd())                    # 当前工作目录
print(os.path.join("data", "train", "a.csv"))  # 拼路径，自动处理 / 和 \

# 判断文件/目录是否存在
print(os.path.exists("test.txt"))     # False
print(os.path.isfile("test.txt"))     # False
print(os.path.isdir("data"))          # False

# 创建/删除目录
os.makedirs("tmp/sub", exist_ok=True) # exist_ok=True：目录已存在不报错 ⬅ 必加
os.removedirs("tmp/sub")              # 删除空目录（从最深层往上删）

# 环境变量：工程中存 API Key、数据库密码，绝对不能硬编码在代码里
os.environ["MY_KEY"] = "secret"
print(os.getenv("MY_KEY", "默认值"))  # 取不到时返回默认值，不会报错

# 遍历目录树（处理数据集文件夹时常用）
# for root, dirs, files in os.walk("data"):
#     for f in files:
#         print(os.path.join(root, f))


# ══════════════════════════════════════════════════════════════
# 二、pathlib —— os.path 的现代替代，推荐优先用这个
# ══════════════════════════════════════════════════════════════
print("\n── pathlib ──")

p = Path(".")                        # 当前目录
print(p.resolve())                   # 绝对路径

# 用 / 拼路径，比 os.path.join 更直观
data_path = Path("data") / "train" / "a.csv"
print(data_path)                     # data/train/a.csv
print(data_path.suffix)              # .csv   文件后缀
print(data_path.stem)                # a      不含后缀的文件名
print(data_path.parent)             # data/train

# 读写文件（小文件用这个最简洁）
tmp = Path("tmp.txt")
tmp.write_text("hello pathlib")      # 写入
print(tmp.read_text())               # 读取
tmp.unlink()                         # 删除文件

# 遍历目录（比 os.walk 更简洁）
# for f in Path("data").rglob("*.csv"):   # 递归找所有 csv
#     print(f)


# ══════════════════════════════════════════════════════════════
# 三、json —— 序列化/反序列化
# ══════════════════════════════════════════════════════════════
print("\n── json ──")

# 【序列化】：Python 对象 → JSON 字符串（用于传输/存储）
data = {"name": "Alice", "scores": [95, 87, 92], "passed": True}
s = json.dumps(data, ensure_ascii=False, indent=2)
# ensure_ascii=False：中文不转义；indent=2：格式化缩进，方便阅读
print(s)

# 【反序列化】：JSON 字符串 → Python 对象（用于读取）
obj = json.loads(s)
print(obj["scores"])                 # [95, 87, 92]  类型还原为 list

# 读写文件
with open("cfg.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)   # dump = dumps + 写文件

with open("cfg.json") as f:
    cfg = json.load(f)                                  # load = 读文件 + loads
print(cfg["name"])                   # Alice

Path("cfg.json").unlink()            # 清理临时文件

# ⚠️ json 只支持：str/int/float/bool/None/list/dict
# tuple 会被转成 list，自定义类需要手动转成 dict


# ══════════════════════════════════════════════════════════════
# 四、re —— 正则表达式
# ══════════════════════════════════════════════════════════════
print("\n── re ──")

text = "订单号：A123，金额：456.78元，日期：2024-01-15"

# search：找第一个匹配，返回 match 对象或 None
m = re.search(r"\d+\.\d+", text)    # r"..." 原始字符串，\ 不转义
if m:
    print(m.group())                 # 456.78

# findall：找所有匹配，返回 list
nums = re.findall(r"\d+", text)
print(nums)                          # ['123', '456', '78', '2024', '01', '15']

# 捕获组 ()：提取结构化数据
m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
if m2:
    print(m2.group(1), m2.group(2), m2.group(3))  # 2024 01 15

# sub：替换
clean = re.sub(r"\d+", "NUM", "价格100元，库存50个")
print(clean)                         # 价格NUM元，库存NUM个

# compile：复用同一个pattern时提前编译，提升性能
pattern = re.compile(r"[A-Z]\d+")   # 编译一次
print(pattern.findall("A123 B456 c789"))  # ['A123', 'B456']


# ══════════════════════════════════════════════════════════════
# 五、sys —— 解释器级别的操作
# ══════════════════════════════════════════════════════════════
print("\n── sys ──")

print(sys.version)                   # Python 版本
print(sys.platform)                  # 操作系统：win32 / linux / darwin

# 算法题竞赛模式：加速标准输入（数据量大时防超时）
# input = sys.stdin.readline          # 比内置 input() 快，刷题偶尔需要

# sys.argv：命令行参数
# python script.py arg1 arg2
# sys.argv = ["script.py", "arg1", "arg2"]
print(sys.argv[0])                   # 当前脚本名

# sys.exit()：立即终止程序，比 raise SystemExit 更语义化
# sys.exit(0)  # 0 表示正常退出，非 0 表示异常退出


# ══════════════════════════════════════════════════════════════
# 六、time / datetime —— 时间处理
# ══════════════════════════════════════════════════════════════
print("\n── time / datetime ──")

# time：性能计时（算法题测速、工程性能分析）
start = time.time()                  # 当前时间戳（秒，浮点数）
sum(range(10**6))
end = time.time()
print(f"耗时：{end - start:.4f}s")

time.sleep(0.1)                      # 休眠0.1秒（模拟网络延迟、限速时用）

# datetime：日期时间的表示与计算
now = datetime.datetime.now()
print(now)                           # 2024-01-15 10:30:00.123456

# 格式化输出
print(now.strftime("%Y-%m-%d %H:%M:%S"))   # 2024-01-15 10:30:00
# %Y 四位年 %m 月 %d 日 %H 时 %M 分 %S 秒

# 字符串 → datetime（解析日志、API时间字段时常用）
dt = datetime.datetime.strptime("2024-01-15", "%Y-%m-%d")
print(dt.year, dt.month, dt.day)     # 2024 1 15

# 时间差计算
d1 = datetime.date(2024, 1, 1)
d2 = datetime.date(2024, 3, 1)
delta = d2 - d1
print(delta.days)                    # 60

# 指定天数后的日期
future = d1 + datetime.timedelta(days=100)
print(future)                        # 2024-04-10