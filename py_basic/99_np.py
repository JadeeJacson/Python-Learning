import numpy as np
import torch

# ============================================================
# 模拟一个小型机器学习数据预处理 + 线性回归的完整流程
# ============================================================

# ==================== 1. 创建数组 ====================
raw = np.array([[2.0, 3.0, np.nan],   # array：从列表创建，nan模拟缺失值
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0],
                [1.0, 2.0, 3.0]])

zeros_col = np.zeros((4, 1))           # zeros：全0列，用于后续拼接
ones_col  = np.ones((4, 1))            # ones：全1列（偏置项）
empty_buf = np.empty((4, 1))           # empty：未初始化，仅占位
full_col  = np.full((4, 1), 99.0)      # full：填充指定值
eye_mat   = np.eye(3)                  # eye：3x3单位矩阵
arange_v  = np.arange(0, 8, 2)        # arange：[0,2,4,6]，步长2
linspace_v= np.linspace(0, 1, 4)      # linspace：[0, 0.33, 0.67, 1.0]，均匀4点
x_grid, y_grid = np.meshgrid(         # meshgrid：生成二维坐标网格
    np.arange(3), np.arange(3))

print("raw:\n", raw)
print("eye_mat:\n", eye_mat)
print("arange:", arange_v)
print("linspace:", linspace_v)
print("meshgrid x:\n", x_grid)

# ==================== 2. 数组基础属性 ====================
print("\n--- 数组属性 ---")
print("ndim :", raw.ndim)    # ndim：维数，raw是二维，输出2
print("shape:", raw.shape)   # shape：(4,3)，4行3列
print("size :", raw.size)    # size：元素总数，4*3=12
print("dtype:", raw.dtype)   # dtype：float64，因为有小数

# ==================== 3. 索引与切片 ====================
print("\n--- 索引切片 ---")
print("第0行      :", raw[0])           # 基础索引：取第0行
print("第1行第2列  :", raw[1, 2])       # 多维索引：取具体元素
print("前2行      :\n", raw[:2])        # 切片：前2行
print("所有行第0列 :", raw[:, 0])       # 切片：取第0列所有元素

# 布尔索引：筛选出非nan的位置
nan_mask = np.isnan(raw)               # nan_mask是同shape的bool数组
print("nan位置:\n", nan_mask)
valid_mask = ~nan_mask                 # ~取反，True表示有效值
print("有效值:", raw[valid_mask])       # 布尔索引：只取有效位置的值

# 花式索引：指定行号列表取多行
rows = np.array([0, 2, 3])
print("第0,2,3行:\n", raw[rows])        # 花式索引：传入索引数组

# np.where：把nan替换为该列均值（先用0占位，后面统计填充）
col_means = np.nanmean(raw, axis=0)    # nanmean忽略nan求均值，axis=0按列
print("列均值:", col_means)
data = np.where(nan_mask, col_means, raw)  # where(条件,真值,假值)：nan处填均值
print("填充后:\n", data)

# ==================== 4. 类型转换 ====================
data = data.astype(np.float32)        # astype：float64→float32，省内存，GPU友好
print("\ndtype转换后:", data.dtype)    # float32

# ==================== 5. 聚合统计 ====================
print("\n--- 聚合统计 ---")
print("每列均值 :", data.mean(axis=0))   # mean(axis=0)：按列求均值，shape(3,)
print("每行求和 :", data.sum(axis=1))    # sum(axis=1)：按行求和，shape(4,)
print("全局标准差:", data.std())         # std：不指定axis则全局计算
print("全局方差  :", data.var())
print("最大值    :", data.max())
print("最大值索引:", data.argmax())      # argmax：返回展平后最大值的索引
print("最小值索引:", data.argmin())
col0_cumsum = data[:, 0].cumsum()       # cumsum：第0列的累积和
print("第0列累积和:", col0_cumsum)
cov_mat = np.cov(data.T)               # cov：协方差矩阵，输入需(特征数,样本数)，故转置
corr_mat = np.corrcoef(data.T)         # corrcoef：相关系数矩阵
print("协方差矩阵:\n", cov_mat)
print("相关系数矩阵:\n", corr_mat)

# ==================== 6. 向量化运算 ====================
print("\n--- 向量化运算 ---")
# ufunc：逐元素操作，底层C实现，远快于for循环
data_clipped = np.clip(data, 2.0, 8.0)  # clip：把值限制在[2,8]，超出部分截断
print("clip后:\n", data_clipped)
print("ceil :\n", np.ceil(data[:2]))     # ceil：向上取整
print("floor:\n", np.floor(data[:2]))   # floor：向下取整
print("round:\n", np.round(data[:2], 1))# round：保留1位小数

# ==================== 7. 广播机制 ====================
print("\n--- 广播机制 ---")
# 标准化：每列减均值除以标准差
col_mean = data.mean(axis=0)   # shape (3,)
col_std  = data.std(axis=0)    # shape (3,)
# data shape(4,3)，col_mean shape(3,)
# 广播规则：从右对齐，(4,3)-(3,)→(3,)扩展为(4,3)后相减
data_norm = (data - col_mean) / col_std
print("标准化后:\n", data_norm)
# 手动验证维度对齐：col_mean被广播成4行重复的(4,3)矩阵

# ==================== 8. 形状操作 ====================
print("\n--- 形状操作 ---")
flat = data_norm.flatten()     # flatten：展平为1维，返回副本
print("flatten shape:", flat.shape)    # (12,)
ravel_v = data_norm.ravel()   # ravel：展平为1维，尽量返回视图（更省内存）
print("ravel shape:", ravel_v.shape)

reshaped = data_norm.reshape(3, 4)    # reshape：(4,3)→(3,4)，元素数不变
print("reshape(3,4):\n", reshaped)

print("transpose:\n", data_norm.T)    # T / transpose：转置，(4,3)→(3,4)

# squeeze / expand_dims：深度学习中处理batch维度常用
single = data_norm[0]                  # shape (3,)，1维
expanded = np.expand_dims(single, axis=0)  # expand_dims：(3,)→(1,3)，增加batch维
print("expand_dims:", expanded.shape)
squeezed = np.squeeze(expanded)        # squeeze：(1,3)→(3,)，删除长度为1的维度
print("squeeze:", squeezed.shape)
newaxis_v = single[np.newaxis, :]     # newaxis：等价expand_dims，(3,)→(1,3)
print("newaxis:", newaxis_v.shape)

# ==================== 9. 拼接与分割 ====================
print("\n--- 拼接分割 ---")
# concatenate：沿已有轴拼接，不新增维度
with_bias = np.concatenate(           # 在列方向(axis=1)拼接偏置列
    [data_norm, ones_col.astype(np.float32)], axis=1)
print("拼接偏置后shape:", with_bias.shape)  # (4,4)

# stack：新增一个维度后拼接
stacked = np.stack([data_norm, data_norm], axis=0)  # (2,4,3)
print("stack shape:", stacked.shape)

# hstack/vstack：快捷拼接
h = np.hstack([data_norm, data_norm])  # 水平拼接，列增加，(4,6)
v = np.vstack([data_norm, data_norm])  # 垂直拼接，行增加，(8,3)
print("hstack:", h.shape, "vstack:", v.shape)

# split：分割
parts = np.split(data_norm, 2, axis=0) # 沿axis=0分成2份，每份(2,3)
print("split后各份shape:", parts[0].shape)

# ==================== 10. 数学函数 ====================
print("\n--- 数学函数 ---")
print("exp:\n", np.exp(data_norm[:2]))   # exp：e的x次方，激活函数softmax会用
print("log:\n", np.log(np.abs(data_norm[:2]) + 1e-8))  # log：自然对数，防止log(0)加小量
print("sqrt:\n", np.sqrt(np.abs(data_norm[:2])))        # sqrt：开方

# dot / inner / outer
w = np.array([0.5, -0.3, 0.8], dtype=np.float32)  # 权重向量，shape(3,)
pred_dot = np.dot(data_norm, w)         # dot：矩阵×向量，(4,3)·(3,)→(4,)
print("dot预测:", pred_dot)
inner_v = np.inner(w, w)               # inner：向量内积，等价dot(w,w)，输出标量
outer_m = np.outer(w, w)               # outer：向量外积，(3,)×(3,)→(3,3)矩阵
print("inner:", inner_v)
print("outer:\n", outer_m)

# ==================== 11. 线性代数 ====================
print("\n--- 线性代数 ---")
X = with_bias.astype(np.float64)       # 切回float64，linalg精度更高
y = np.array([1.0, 2.0, 3.0, 4.0])    # 目标值

# matmul / @：矩阵乘法（推荐用@，更简洁）
XtX = X.T @ X                          # X转置乘X，(4,4)
print("X.T @ X shape:", XtX.shape)

# solve：求解线性方程组，比inv更稳定
# 最小二乘解：w = (X^T X)^{-1} X^T y
w_ls = np.linalg.solve(XtX, X.T @ y)  # solve(A, b)：解Aw=b
print("最小二乘权重:", w_ls)

# inv：求逆矩阵（了解原理，实际用solve更好）
XtX_inv = np.linalg.inv(XtX)
print("inv结果与solve接近:", np.allclose(XtX_inv @ (X.T @ y), w_ls))

# norm：范数，正则化/梯度裁剪常用
print("w L2范数:", np.linalg.norm(w_ls))         # 默认L2范数
print("w L1范数:", np.linalg.norm(w_ls, ord=1))  # L1范数

# eig：特征值分解
eigvals, eigvecs = np.linalg.eig(XtX)  # eig：返回特征值和特征向量
print("特征值:", eigvals)

# svd：奇异值分解，PCA降维核心
U, S, Vt = np.linalg.svd(X, full_matrices=False)  # full_matrices=False为经济型SVD
print("SVD: U", U.shape, "S", S.shape, "Vt", Vt.shape)

# ==================== 12. 随机模块 ====================
print("\n--- 随机模块 ---")
np.random.seed(42)                          # seed：固定随机种子，实验可复现
noise = np.random.randn(4)                  # randn：标准正态分布N(0,1)
print("randn噪声:", noise)
rand_v = np.random.rand(4)                  # rand：均匀分布U(0,1)
normal_v = np.random.normal(0, 0.1, (4,3)) # normal：指定均值0、标准差0.1
uniform_v = np.random.uniform(-1, 1, 4)    # uniform：指定范围均匀分布
idx = np.random.choice(4, size=3, replace=False)  # choice：不放回随机采样3个索引
print("随机采样索引:", idx)
arr_shuf = np.arange(4)
np.random.shuffle(arr_shuf)                 # shuffle：原地打乱顺序
print("shuffle后:", arr_shuf)

# ==================== 13. 排序与搜索 ====================
print("\n--- 排序搜索 ---")
pred = np.dot(data_norm, w)               # 用之前的权重做预测，shape(4,)
print("预测值:", pred)
sorted_pred = np.sort(pred)               # sort：升序排列，返回新数组
print("排序后:", sorted_pred)
sort_idx = np.argsort(pred)               # argsort：返回排序后对应的原始索引
print("argsort索引:", sort_idx)           # 用于间接排序其他数组

top2_idx = np.argpartition(pred, -2)[-2:]  # argpartition：找最大2个的索引，比全排序快
print("Top2索引:", top2_idx)

uniq, counts = np.unique(                  # unique：去重，return_counts返回出现次数
    np.array([1,2,2,3,3,3]), return_counts=True)
print("unique:", uniq, "counts:", counts)

insert_pos = np.searchsorted(              # searchsorted：二分查找插入位置
    sorted_pred, 0.5)
print("0.5应插入位置:", insert_pos)

# ==================== 14. 内存布局 ====================
print("\n--- 内存布局 ---")
a = data_norm
b = a.view()          # view：共享内存，修改b会影响a
c = a.copy()          # copy：完全独立副本，互不影响
b[0, 0] = 999.0
print("修改view后a[0,0]:", a[0, 0])   # 999.0，共享内存
c[0, 0] = -999.0
print("修改copy后a[0,0]:", a[0, 0])   # 仍是999.0，不影响原数组

print("a是否C连续:", a.flags['C_CONTIGUOUS'])  # C order：行优先，默认
print("a的stride:", a.strides)                  # stride：每步跳过的字节数

a_fortran = np.asfortranarray(a)               # F order：列优先
print("F order连续:", a_fortran.flags['F_CONTIGUOUS'])

# ==================== 15. IO操作 ====================
print("\n--- IO操作 ---")
np.save("data_norm.npy", data_norm)             # save：保存单个数组为.npy
loaded = np.load("data_norm.npy")               # load：加载.npy文件
print("load后相等:", np.allclose(data_norm, loaded))

np.savez("arrays.npz", X=X, y=y)               # savez：保存多个数组到.npz
npz = np.load("arrays.npz")
print("savez keys:", list(npz.keys()))           # ['X', 'y']

np.savetxt("data.csv", data_norm, delimiter=",", fmt="%.4f")  # savetxt：保存为CSV
loaded_txt = np.loadtxt("data.csv", delimiter=",")            # loadtxt：读取CSV
print("loadtxt shape:", loaded_txt.shape)

# ==================== 16. 库衔接 ====================
print("\n--- 库衔接 ---")
py_list = data_norm.tolist()                   # tolist：ndarray→Python列表
print("tolist类型:", type(py_list))

import pandas as pd
df = pd.DataFrame(data_norm, columns=["f1","f2","f3"])
arr_from_df = df.to_numpy()                    # to_numpy：DataFrame→ndarray（推荐）
arr_values  = df.values                        # values：同上，旧写法
print("to_numpy shape:", arr_from_df.shape)

tensor = torch.from_numpy(                     # from_numpy：ndarray→Tensor，零拷贝共享内存
    data_norm.astype(np.float32))
print("tensor:", tensor)
print("tensor dtype:", tensor.dtype)           # torch.float32
back_to_np = tensor.numpy()                    # .numpy()：Tensor→ndarray，同样零拷贝
print("back to numpy shape:", back_to_np.shape)