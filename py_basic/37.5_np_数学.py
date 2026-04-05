"""
【NumPy 数学与线性代数：AI 炼丹的底层引擎】
请在 VS Code 中单步调试，观察矩阵形状和数值的变化！
"""
import numpy as np
import numpy.linalg as LA # 线性代数模块通常被简写为 LA

print("="*10, "1. 基础数学与防爆雷技巧 (exp, log)", "="*10)

logits = np.array([1.0, 2.0, 5.0])
# a=1: exp (指数运算) - 常用于 Softmax 计算概率
# 缺点：极易发生数值溢出 (Exploding)
probs = np.exp(logits) / np.sum(np.exp(logits))
print(f"Softmax 概率分布: {probs}")

# a=2: log (对数运算) - 常用于计算 Loss
# 💣 核弹级大坑：千万不要对 0 取 log，会得到 -inf！
safe_probs = np.array([0.0, 0.5, 0.5])
# 业界标准最佳实践：永远在 log 里加一个极小的常数 (如 1e-9) 防止系统崩溃
loss = -np.log(safe_probs + 1e-9) 
print(f"安全的 Log Loss: {loss}")


print("\n"+"="*10, "2. 向量魔法：dot 与 outer", "="*10)

v1 = np.array([1, 2, 3])
v2 = np.array([0, 1, 0])

# a=3: dot (点积) - 衡量相似度。1D 数组点积就是一个标量！
similarity = np.dot(v1, v2)
print(f"向量点积 (v1 在 v2 方向的重合度): {similarity}")

# a=4: outer (外积) - 无中生有，从小变大
# 长度 3 的向量 outer 长度 2 的向量，生成 3x2 的矩阵 (九九乘法表原理)
v3 = np.array([10, 20])
outer_mat = np.outer(v1, v3)
print(f"向量外积生成的矩阵:\n{outer_mat}")


print("\n"+"="*10, "3. 线性代数核心：@ 与 solve", "="*10)

X = np.array([[1, 2], [3, 4]]) # 模拟输入特征 (2个样本, 2个特征)
W = np.array([[0.1, 0.2], [0.3, 0.4]]) # 模拟模型权重

# a=5: matmul 矩阵乘法
# 💡 现代 Python 最佳实践：永远使用 @ 符号替代 np.matmul 或 np.dot！
Y = X @ W
print(f"神经网络前向传播 X @ W:\n{Y}")

# a=6: 解线性方程组 Ax = b (求未知数 x)
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

# ❌ 菜鸟写法：x = LA.inv(A) @ b  (求逆极慢，且容易引发浮点精度灾难)
# ✅ 大厂写法：使用 solve，底层调用 LAPACK 优化库，快且稳！
x_optimal = LA.solve(A, b)
print(f"安全求解线性方程组 (Ax=b) 的 x: {x_optimal}")


print("\n"+"="*10, "4. 高阶武学：特征值、SVD 与 范数", "="*10)

# a=7: norm (范数) - 计算向量或矩阵的“大小/长度”
vector = np.array([3, 4])
# 默认计算 L2 范数 (欧几里得距离，勾股定理)
print(f"向量的 L2 范数 (长度): {LA.norm(vector)}")

# a=8: SVD (奇异值分解) - 一切矩阵皆可拆！
M = np.array([[1, 2], [3, 4], [5, 6]])
# 将 3x2 的矩阵拆成：正交矩阵 U，奇异值数组 S，正交矩阵 V 的转置
U, S, V_T = LA.svd(M, full_matrices=False)

print(f"\nSVD 分解得到的奇异值 (代表了数据中最重要的成分权重): {S}")
# 重构原矩阵 (验证 SVD 的正确性)
# 注意：np.diag(S) 是把 1D 的 S 变成对角矩阵
M_reconstructed = U @ np.diag(S) @ V_T
print(f"利用 SVD 碎片重构后的原矩阵:\n{np.round(M_reconstructed)}")