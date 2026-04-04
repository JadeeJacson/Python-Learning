"""
【NumPy 兵工厂：九大数组创建神技】
请在 VS Code 中运行，直观感受矩阵生成的速度与美感！
"""
import numpy as np

print("="*10, "1. 纯色量产与毛坯房 (zeros, ones, full, empty)", "="*10)

# a=1: np.zeros 和 np.ones
# ⚠️ 注意：shape 必须是一个元组 (tuple)，所以会有两层括号！
zeros_mat = np.zeros((2, 3)) 
ones_mat = np.ones((2, 3), dtype=np.int32) # 指定为整数，默认是 float64
print(f"全 0 矩阵:\n{zeros_mat}")
print(f"全 1 整数矩阵:\n{ones_mat}")

# a=2: np.full (填充指定数值)
full_mat = np.full((2, 2), 3.14)
print(f"\n全 3.14 矩阵:\n{full_mat}")

# a=3: np.empty (极速毛坯房)
# 分配内存极快，但内容是随机的内存垃圾 (取决于这块内存在分配前存过什么)
empty_mat = np.empty((2, 2))
print(f"\nEmpty 矩阵 (里面的数字是毫无意义的内存残留！):\n{empty_mat}")


print("\n"+"="*10, "2. 单位矩阵 (eye)", "="*10)
# 创建一个 3x3 的单位矩阵。在线性代数中，任何矩阵乘以它，都等于原矩阵。
eye_mat = np.eye(3)
print(f"3x3 单位矩阵:\n{eye_mat}")


print("\n"+"="*10, "3. 等差标尺 (arange vs linspace)", "="*10)
# a=4: np.arange (起始值, 结束值, 步长) -> 左闭右开 [start, end)
# 从 0 开始，每次加 2，到 10 停止 (不包含 10)
range_arr = np.arange(0, 10, 2)
print(f"arange 数组: {range_arr}")

# a=5: np.linspace (起始值, 结束值, 元素总个数) -> 默认双闭 [start, end]
# 从 0 到 1 之间，精确地切出 5 个点
lin_arr = np.linspace(0, 1, 5)
print(f"linspace 数组: {lin_arr}")


print("\n"+"="*10, "4. 时空坐标网 (meshgrid)", "="*10)
# a=6: 假设我们在玩战棋游戏，X轴坐标是 1,2,3，Y轴坐标是 10,20
x = np.array([1, 2, 3])
y = np.array([10, 20])

# meshgrid 会生成两张底片，叠在一起就构成了网格上所有的坐标对！
X, Y = np.meshgrid(x, y)

print("X 网格底片 (每行都一样):")
print(X)
print("\nY 网格底片 (每列都一样):")
print(Y)

print("\n组合出的实际坐标点：")
# 遍历网格提取坐标
for i in range(Y.shape[0]):
    for j in range(X.shape[1]):
        print(f"({X[i,j]}, {Y[i,j]})", end=" ")
    print()