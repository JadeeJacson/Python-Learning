"""
【Python 标准库：大厂工程与算法刷题的黄金 API】
请在 VS Code 中运行。
代码分为“工程基建”和“算法核武器”两部分。
"""
import os
import sys
import math
import random
import time
import json
import re
from datetime import datetime
from pathlib import Path
from collections import Counter, deque
import itertools
from functools import lru_cache

print("="*10, "第一战区：工程基建 (文件、系统、时间、JSON、正则)", "="*10)

# a=1: pathlib 与 os (现代路径操作)
# 永远不要再用字符串拼接路径 (如 dir + "/" + file)！用 pathlib！
current_dir = Path.cwd() # 获取当前路径
mock_file = current_dir / "dataset" / "config.json" # 用 / 符号直接拼接路径，极其优雅！
print(f"[Pathlib] 模拟生成的文件路径: {mock_file}")
print(f"[Pathlib] 提取文件名: {mock_file.name}, 提取后缀: {mock_file.suffix}")

# a=2: json (配置文件读写)
# 模拟深度学习模型的超参数保存
hyperparams = {"learning_rate": 0.001, "batch_size": 32, "model": "ResNet"}
json_str = json.dumps(hyperparams, indent=4) # indent=4 让输出格式化，美观易读
print(f"[JSON] 序列化后的配置:\n{json_str}")

# a=3: re (正则表达式)
# 工程场景：从脏乱的网页文本中提取所有的邮箱地址
text = "联系管理员 admin@google.com 或者 hr@openai.com 获取权限。"
# 使用 re.compile 预编译正则规则，比直接用 re.findall 性能高很多！
email_pattern = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+')
emails = email_pattern.findall(text)
print(f"[正则] 提取到的邮箱: {emails}")

# a=4: time 与 datetime
# time.perf_counter() 是大厂用来测试代码运行时间的最高精度时钟！
start_time = time.perf_counter()
time.sleep(0.1) # 模拟耗时操作
cost = time.perf_counter() - start_time
print(f"[时间] 代码执行耗时: {cost:.4f} 秒")
print(f"[日期] 当前人类可读时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


print("\n"+"="*10, "第二战区：算法核武器 (刷题必背！)", "="*10)

# a=5: collections (超级数据结构)
print("--- collections ---")
# 1. Counter (计数器)：一句话统计词频，直接替代手写 for 循环和 dict
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
word_counts = Counter(words)
print(f"词频统计: {word_counts}")
print(f"出现最多的前1个词: {word_counts.most_common(1)}")

# 2. deque (双端队列)：LeetCode 广度优先搜索 (BFS) 必备！
# 💣 严禁在列表头部插入或弹出数据 (list.pop(0))，那是 O(N) 的灾难！
# 必须用 deque，它的两端操作都是 O(1) 的极致性能。
queue = deque([1, 2, 3])
queue.append(4)      # 尾部进
queue.popleft()      # 头部出 (极快！)
print(f"BFS 队列状态: {queue}")


# a=6: itertools (迭代器组装车间)
print("\n--- itertools ---")
# 算法题：求 3 个元素的全排列和组合
items = ['A', 'B', 'C']
# permutations: 全排列 (A,B,C 和 B,A,C 算两种)
perms = list(itertools.permutations(items, 2)) 
# combinations: 组合 (A,B 和 B,A 算一种)
combs = list(itertools.combinations(items, 2))
print(f"全排列: {perms}")
print(f"组合: {combs}")


# a=7: functools.lru_cache (备忘录/缓存魔法)
print("\n--- functools ---")
# 算法题：斐波那契数列（递归树）。如果不加缓存，n=40 就会卡死。
# 加上 @lru_cache()，它会自动把算过的输入参数和结果存在内存里，
# 下次遇到同样的参数，直接 O(1) 返回结果！瞬间将时间复杂度从指数级降为 O(N)！
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"加了魔法缓存的斐波那契(100): {fibonacci(100)} (瞬间算完！)")

#不完整，需拓展

#以及下一节另学pip，conda