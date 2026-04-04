"""
【NumPy 高阶魔法：广播机制与向量化运算】
请在 VS Code 中运行，体会“不写 for 循环”的丝滑与极速！
"""
import numpy as np
import math

print("="*10, "1. 广播机制：空间拉伸魔法", "="*10)

# a=1: 矩阵与标量的广播 (最基础)
mat = np.array([[1, 2, 3], [4, 5, 6]]) # shape (2, 3)
# 这里的 10 也是一个标量，被广播成了 (2, 3) 的全 10 矩阵
print(f"矩阵加标量:\n{mat + 10}")

# a=2: 矩阵与向量的广播
row_vec = np.array([10, 20, 30])       # shape (3,) 相当于 (1, 3)
# 广播规则：从右往左看，列数都是 3。行数一个是 2，一个是缺失(当作1)。因此行向量被垂直拉伸复制！
print(f"\n矩阵加上行向量 (每行都加了 10,20,30):\n{mat + row_vec}")

col_vec = np.array([[100], [200]])     # shape (2, 1)
# 广播规则：行数都是 2。列数一个是 3，一个是 1。因此列向量被水平拉伸复制！
print(f"\n矩阵加上列向量 (第一行全加100，第二行全加200):\n{mat + col_vec}")

# a=3: 令人炸裂的降维打击 (两根一维面条，变成二维网格)
# (3, 1) 的列向量 加上 (1, 3) 的行向量，竟然生成了 (3, 3) 的矩阵！
A = np.array([[1], [2], [3]])
B = np.array([10, 20, 30])
print(f"\n列向量 + 行向量 (奇迹般的网格生成):\n{A + B}")


print("\n"+"="*10, "2. Ufunc 与数值清洗魔法", "="*10)

# 假设这是一批传感器的原始数据，包含负数、小数、甚至极端异常值
sensor_data = np.array([-5.2, 1.8, 2.5, 999.9, 3.1])

# a=4: clip (削峰填谷，异常值清洗神器)
# 把所有低于 0 的强行拉到 0，高于 5 的强行砍到 5
clipped_data = np.clip(sensor_data, a_min=0, a_max=5)
print(f"原数据: {sensor_data}")
print(f"clip(0, 5) 清洗后: {clipped_data}")

# a=5: 数值舍入 (Ufunc 群体施法)
print(f"\nceil (向上取整的天花板):  {np.ceil(sensor_data)}")
print(f"floor (向下取整的地板):    {np.floor(sensor_data)}")
print(f"round (四舍五入到最近的偶数): {np.round(sensor_data)}")

# a=6: 速度碾压测试 (为何千万别写 for 循环)
# 计算一百万个数字的平方根
big_data = np.arange(1000000)

import time
start = time.time()
# 纯 Python 的傻瓜循环
[math.sqrt(x) for x in big_data] if 'math' in globals() else [x**0.5 for x in big_data]
print(f"\nPython for 循环耗时: {time.time() - start:.4f} 秒")

start = time.time()
# NumPy Ufunc 向量化全屏秒杀
np.sqrt(big_data)
print(f"NumPy Ufunc 耗时: {time.time() - start:.4f} 秒 (快了近百倍！)")