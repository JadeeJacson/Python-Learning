"""
【NumPy 基础：军用集装箱的五大核心指标】
请在 VS Code 中运行，体会 ndarray 的结构美学！
"""
import numpy as np

print("="*10, "1. 杂物箱 vs 军用集装箱", "="*10)

# Python 杂物箱：啥都能装，但内存极其碎片化
py_list = [1, "AI", 3.14]
print(f"Python 列表: {py_list}")

# NumPy 集装箱：强制统一类型 (同质化)
# a=1: 注意！当我们把整数和浮点数混装时，NumPy 会自动“向上兼容” (Upcasting)
np_array = np.array([1, 2, 3.14])
print(f"NumPy 数组: {np_array}") 
# 你会发现 1 和 2 自动变成了 1.0 和 2.0，这就是 dtype 的严谨性！


print("\n"+"="*10, "2. 解剖 2D 矩阵 (核心四大属性)", "="*10)

# a=2: 创建一个 2 行 3 列的矩阵 (注意括号的嵌套！)
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print(f"【数组本体】:\n{matrix}")

# 核心指标 1：ndim (维度数)
# 快速判断法：看打印出来的最左边有几个连续的 '[' 括号，就是几维！
print(f"-> ndim  (维度数): {matrix.ndim} 维")

# 核心指标 2：shape (形状)
# AI 工程师的命根子。报错 90% 都是 shape 对不上。
print(f"-> shape (形状):   {matrix.shape} (即 {matrix.shape[0]} 行, {matrix.shape[1]} 列)")

# 核心指标 3：size (总元素个数)
print(f"-> size  (总容量): {matrix.size} 个元素")

# 核心指标 4：dtype (数据类型)
print(f"-> dtype (类型):   {matrix.dtype}")


print("\n"+"="*10, "3. 手动指定与修改 dtype", "="*10)

# a=3: 深度学习中，为了省显存，经常把 float64 降级成 float32 甚至 float16
# 在创建时强行指定类型，节省 50% 内存！
memory_saving_array = np.array([1.1, 2.2, 3.3], dtype=np.float32)
print(f"省内存的数组类型: {memory_saving_array.dtype}")

# a=4: 如果数组已经建好了，用 astype() 进行类型转换 (会返回一个新数组)
int_array = memory_saving_array.astype(np.int32)
print(f"强制转为整数后: {int_array} (注意：小数部分被直接抹除了！)")