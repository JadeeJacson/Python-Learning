# ============================================================
# 随机模块 & 类型转换 完整讲解
# ============================================================
import numpy as np

# ============================================================
# PART 1: 随机种子 np.random.seed()
# ============================================================
# 【核心概念】计算机的"随机"是伪随机，seed固定后每次结果一样
# 算法题/实验中常用，保证结果可复现

np.random.seed(42)
print(np.random.rand(3))   # [0.374 0.951 0.732]

np.random.seed(42)         # 重置同一个seed
print(np.random.rand(3))   # 完全一样！[0.374 0.951 0.732]

# ============================================================
# PART 2: rand vs randn
# ============================================================

# rand: 均匀分布，范围 [0, 1)，每个值等概率出现
a = np.random.rand(4)
print("rand:", a)          # 如 [0.37 0.95 0.73 0.59]

# rand生成二维数组（常用于初始化权重矩阵）
mat = np.random.rand(3, 4) # 3行4列，值在[0,1)
print("rand 2D shape:", mat.shape)

# randn: 标准正态分布，均值=0，标准差=1，大多数值在[-3, 3]
b = np.random.randn(4)
print("randn:", b)         # 如 [0.49 -0.14 0.31 1.46]，可能出现负数！

# randn生成二维（神经网络权重初始化常用）
mat2 = np.random.randn(3, 4)
print("randn 2D shape:", mat2.shape)

# ============================================================
# PART 3: normal —— 自定义均值和标准差的正态分布
# ============================================================
# np.random.normal(loc=均值, scale=标准差, size=形状)

scores = np.random.normal(loc=75, scale=10, size=5)  # 模拟考试成绩
print("normal scores:", scores.round(1))  # 如 [72.1 85.3 68.9 79.2 74.5]

# randn 和 normal 的关系：randn() 等价于 normal(0, 1)
# randn(3,3) == normal(loc=0, scale=1, size=(3,3))

# ============================================================
# PART 4: uniform —— 自定义范围的均匀分布
# ============================================================
# np.random.uniform(low=下界, high=上界, size=形状)

u = np.random.uniform(low=-1, high=1, size=5)  # [-1, 1) 均匀分布
print("uniform:", u.round(3))

# 对比：rand()  等价于  uniform(0, 1)

# ============================================================
# PART 5: choice —— 从数组中随机采样
# ============================================================
# np.random.choice(a, size, replace=True/False, p=概率分布)

arr = np.array([10, 20, 30, 40, 50])

# replace=True（默认）：有放回抽样，同一元素可被多次抽到
c1 = np.random.choice(arr, size=3, replace=True)
print("有放回:", c1)

# replace=False：无放回，不会重复（size不能超过arr长度！）
c2 = np.random.choice(arr, size=3, replace=False)
print("无放回:", c2)

# p 指定每个元素被选中的概率（概率之和必须=1）
c3 = np.random.choice(arr, size=3, p=[0.5, 0.1, 0.1, 0.1, 0.2])
print("加权采样:", c3)  # 10被抽到的概率最高

# 直接传入整数n：等价于从 np.arange(n) 中抽取（算法题常用！）
idx = np.random.choice(10, size=3, replace=False)  # 从0~9中抽3个不重复索引
print("随机索引:", idx)

# ============================================================
# PART 6: shuffle —— 原地打乱顺序
# ============================================================
# 注意：shuffle 直接修改原数组，无返回值！

data = np.array([1, 2, 3, 4, 5])
np.random.shuffle(data)    # 原地修改，返回None
print("shuffled:", data)   # data本身被打乱

# 常见错误写法（会得到None）：
# data = np.random.shuffle(data)  ← 错！data变成None了

# 如果不想改变原数组，先copy再shuffle
original = np.array([1, 2, 3, 4, 5])
copy = original.copy()
np.random.shuffle(copy)
print("original保持不变:", original)
print("copy被打乱:", copy)

# ============================================================
# PART 7: 类型转换 astype
# ============================================================
# 【核心概念】astype 生成新数组（不修改原数组），需要用变量接收

raw = np.array([1.7, 2.9, 3.1, 4.8])

# float64 → int32：直接截断（不是四舍五入！）
as_int32 = raw.astype(np.int32)
print("int32:", as_int32)   # [1 2 3 4] ← 注意是截断不是四舍五入

# int → float32（神经网络常用，省内存，牺牲一点精度）
ints = np.array([1, 2, 3, 4])
as_f32 = ints.astype(np.float32)
print("float32:", as_f32)   # [1. 2. 3. 4.]

# → bool_：0变False，非0变True
as_bool = ints.astype(np.bool_)
print("bool_:", as_bool)    # [True True True True]

zero_mix = np.array([0, 1, 0, 3, -1])
print("含0的bool:", zero_mix.astype(np.bool_))  # [False True False True True]

# ============================================================
# PART 8: 各类型内存大小对比（实际工程中的选型依据）
# ============================================================
# float64: 64位，精度高，默认类型，占8字节
# float32: 32位，精度略低，占4字节 ← 深度学习常用，省显存
# int64:   64位整数，范围大，占8字节
# int32:   32位整数，范围约±21亿，占4字节
# bool_:   布尔型，占1字节

for dtype in [np.float64, np.float32, np.int64, np.int32, np.bool_]:
    arr_tmp = np.array([1, 2, 3], dtype=dtype)
    print(f"{str(dtype.__name__):8s} → itemsize={arr_tmp.itemsize}字节, dtype={arr_tmp.dtype}")

# ============================================================
# PART 9: 实战场景 —— 模拟数据集划分（算法题/ML常用）
# ============================================================
np.random.seed(0)

data = np.arange(10)           # 模拟10个样本的索引
labels = (np.random.rand(10) > 0.5).astype(np.int32)  # 随机0/1标签

# 无放回抽取80%作为训练集索引
train_idx = np.random.choice(len(data), size=8, replace=False)
test_idx  = np.array([i for i in range(len(data)) if i not in train_idx])

print("训练集索引:", sorted(train_idx))
print("测试集索引:", test_idx)
print("训练集标签:", labels[train_idx])