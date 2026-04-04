"""
【NumPy 进阶：外科手术与空间魔法】
请在 VS Code 中运行，仔细观察矩阵形状和内容的变化！
"""
import numpy as np

print("="*10, "1. 索引与切片：手术刀与点名册", "="*10)
# 创建一个 3行4列 的矩阵
mat = np.arange(12).reshape((3, 4))
print(f"原矩阵:\n{mat}")

# a=1: 基础切片：获取前 2 行，后 2 列
print(f"\n基础切片:\n{mat[0:2, 2:4]}")

# a=2: 布尔索引 (极其重要！)
# 找出矩阵中所有偶数
mask = (mat % 2 == 0) # 产生一个全是 True/False 的同形状矩阵
print(f"\n布尔索引(过滤偶数): {mat[mask]} (注意：输出变成了 1D 数组)")

# a=3: 花式索引 (传入列表点名)
# 只要第 0 行和第 2 行
print(f"\n花式索引:\n{mat[[0, 2], :]}")

# a=4: np.where(条件, 为真时的值, 为假时的值)
# 把所有大于 5 的变成 99，其余变成 -1
where_res = np.where(mat > 5, 99, -1)
print(f"\nnp.where 替换结果:\n{where_res}")


print("\n"+"="*10, "2. 形状魔法：折叠与降维", "="*10)
arr = np.array([[1, 2], [3, 4], [5, 6]]) # 3x2 矩阵

# a=5: 压平为 1D
print(f"flatten (碾平): {arr.flatten()}")

# a=6: 转置 (行变列)
print(f"转置 arr.T:\n{arr.T}")

# a=7: 维度的充气与抽气 (AI模型最常用！)
# 假设这是一张灰度图，shape 是 (3, 2)。AI 框架要求输入必须带通道数 (3, 2, 1)
expanded = np.expand_dims(arr, axis=2) # 或者用 arr[:, :, np.newaxis]
print(f"\n扩维后 shape: {expanded.shape}")

# 把刚才那个多余的 1 维捏瘪
squeezed = expanded.squeeze()
print(f"挤压后 shape: {squeezed.shape}")


print("\n"+"="*10, "3. 拼接与分割：乐高积木", "="*10)
A = np.array([[1, 1], [1, 1]])
B = np.array([[2, 2], [2, 2]])

# a=8: concatenate / vstack (垂直) / hstack (水平)
print(f"vstack (上下垂直拼接):\n{np.vstack((A, B))}") 
print(f"hstack (左右水平拼接):\n{np.hstack((A, B))}")

# a=9: stack 升维叠加
# 把两个 2x2 的矩阵，像叠纸一样叠成一个 2x2x2 的三维张量
stacked = np.stack((A, B), axis=0)
print(f"\nstack 后 shape: {stacked.shape}")

# a=10: split 分割
# 把上面那个垂直拼接出来的 4x2 矩阵，拦腰锯成两半
C = np.vstack((A, B))
split_res = np.split(C, 2, axis=0)
print(f"\nsplit 锯开后的第一部分:\n{split_res[0]}")