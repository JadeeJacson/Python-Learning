# ============================================================
# 内存布局 / IO操作 / 库衔接 完整讲解
# ============================================================
import numpy as np
import pandas as pd
import torch
import os

# ============================================================
# PART 1: view vs copy —— 共享内存 vs 独立副本
# ============================================================
# 【核心概念】view和原数组共享同一块内存，修改一个另一个也变
#            copy是完全独立的新内存，互不影响

original = np.array([1, 2, 3, 4, 5])

v = original.view()    # 视图：共享内存
c = original.copy()    # 副本：独立内存

v[0] = 999             # 修改view
print("修改view后 original:", original)  # [999 2 3 4 5] ← original也变了！
print("修改view后 copy:    ", c)         # [1 2 3 4 5]   ← copy不受影响

# 判断是否共享内存
print("view共享内存:", np.shares_memory(original, v))  # True
print("copy共享内存:", np.shares_memory(original, c))  # False

# 【重要】切片操作默认是view，不是copy！
original = np.array([1, 2, 3, 4, 5])
sliced = original[1:4]           # 切片 → view
sliced[0] = 999
print("切片修改后original:", original)  # [1 999 3 4 5] ← 原数组被改了！

# 如果不想影响原数组，切片后显式copy
safe_slice = original[1:4].copy()

# ============================================================
# PART 2: stride —— 步长，理解内存访问的核心
# ============================================================
# 【核心概念】stride表示"沿某个轴移动一步，需要跳过多少字节"
# 理解stride是理解view/contiguous/性能优化的基础

arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.int32)  # int32 = 4字节/元素

print("shape:  ", arr.shape)    # (2, 3)
print("strides:", arr.strides)  # (12, 4)
# 行方向跳12字节(=3个int32) → 移到下一行
# 列方向跳4字节(=1个int32)  → 移到下一列

# 转置只是交换stride，不移动数据！
t = arr.T
print("转置strides:", t.strides)  # (4, 12) ← 只是把(12,4)反过来，内存没动

# ============================================================
# PART 3: contiguous —— 内存连续性
# ============================================================
# 【核心概念】C order(行优先)和F order(列优先)都算连续
# 但转置后的数组既不是C连续也不是F连续（strides不符合规律）

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("原数组 C连续:", arr.flags['C_CONTIGUOUS'])    # True
print("原数组 F连续:", arr.flags['F_CONTIGUOUS'])    # False

t = arr.T
print("转置后 C连续:", t.flags['C_CONTIGUOUS'])      # False ← 不连续
print("转置后 F连续:", t.flags['F_CONTIGUOUS'])      # True

# 用 np.ascontiguousarray 强制变成C连续（某些操作要求连续内存）
t_cont = np.ascontiguousarray(t)
print("强制连续后 C连续:", t_cont.flags['C_CONTIGUOUS'])  # True

# ============================================================
# PART 4: C order vs F order —— 行优先 vs 列优先
# ============================================================
# C order(默认): 行优先，内存中一行排完再排下一行 → [1,2,3,4,5,6]
# F order:       列优先，内存中一列排完再排下一列 → [1,4,2,5,3,6]

arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')

print("C order内存顺序:", arr_c.ravel(order='C'))  # [1 2 3 4 5 6]
print("F order内存顺序:", arr_f.ravel(order='F'))  # [1 4 2 5 3 6]

# reshape时 order 参数影响元素填充顺序
data = np.arange(6)
print("C reshape:\n", data.reshape(2, 3, order='C'))  # 按行填充（默认）
# [[0 1 2]
#  [3 4 5]]
print("F reshape:\n", data.reshape(2, 3, order='F'))  # 按列填充
# [[0 2 4]
#  [1 3 5]]

# ============================================================
# PART 5: IO操作 —— save / load / savez / savetxt / loadtxt
# ============================================================
os.makedirs("/tmp/np_io", exist_ok=True)

arr = np.array([[1.0, 2.0], [3.0, 4.0]])
labels = np.array([0, 1, 0, 1])

# ---- save / load：保存单个数组为 .npy（二进制，保留dtype和shape）----
np.save("/tmp/np_io/arr.npy", arr)
loaded = np.load("/tmp/np_io/arr.npy")
print("load结果:", loaded)         # [[1. 2.] [3. 4.]]
print("dtype保留:", loaded.dtype)  # float64 ← 二进制格式完整保留信息

# ---- savez：保存多个数组到一个 .npz 文件（zip压缩）----
np.savez("/tmp/np_io/data.npz", features=arr, labels=labels)
npz = np.load("/tmp/np_io/data.npz")
print("npz的keys:", list(npz.keys()))         # ['features', 'labels']
print("features:\n", npz['features'])
print("labels:  ", npz['labels'])

# savez_compressed：压缩率更高，适合大数组
np.savez_compressed("/tmp/np_io/data_compressed.npz", features=arr, labels=labels)

# ---- savetxt / loadtxt：保存为可读文本（CSV格式）----
# savetxt(文件路径, 数组, delimiter=分隔符, fmt=格式, header=表头)
np.savetxt("/tmp/np_io/arr.csv", arr,
           delimiter=',',
           fmt='%.2f',           # 保留2位小数
           header='col1,col2',   # 表头（会加#前缀）
           comments='')          # 不加#前缀

loaded_txt = np.loadtxt("/tmp/np_io/arr.csv",
                        delimiter=',',
                        skiprows=1)   # 跳过表头行
print("loadtxt结果:\n", loaded_txt)

# 格式对比总结：
# .npy  → 速度快，保留dtype，不可读，单数组
# .npz  → 速度快，保留dtype，不可读，多数组，有压缩
# .csv  → 速度慢，dtype丢失，可读，适合与Excel/pandas交换数据

# ============================================================
# PART 6: 库衔接 —— NumPy ↔ Python List
# ============================================================
arr = np.array([[1, 2, 3], [4, 5, 6]])

lst = arr.tolist()                     # ndarray → Python 原生 list
print("tolist:", lst)                  # [[1, 2, 3], [4, 5, 6]]
print("类型:", type(lst))              # <class 'list'>
print("元素类型:", type(lst[0][0]))    # <class 'int'> ← 不是np.int64，是原生int

# 注意：tolist()后元素是Python原生类型，JSON序列化时必须用tolist()
# np.int64 不能直接json.dumps，但 int 可以
import json
# json.dumps(arr.tolist())   ← 正确
# json.dumps(arr.tolist())   ← 错误，np.int64不可序列化

# ============================================================
# PART 7: 库衔接 —— NumPy ↔ Pandas
# ============================================================
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4.0, 5.0, 6.0]})

# DataFrame → ndarray
arr_from_df = df.values          # 方式1：.values（旧式，仍常用）
arr_from_df2 = df.to_numpy()     # 方式2：.to_numpy()（推荐，可指定dtype）
print("values:\n",    arr_from_df)
print("to_numpy:\n",  arr_from_df2)

# to_numpy 的优势：可以指定dtype，values不行
arr_f32 = df.to_numpy(dtype=np.float32)
print("指定dtype:", arr_f32.dtype)   # float32

# 单列 Series → ndarray
col = df['A'].to_numpy()
print("列转numpy:", col)             # [1 2 3]

# ndarray → DataFrame
arr = np.array([[1, 2], [3, 4], [5, 6]])
df2 = pd.DataFrame(arr, columns=['x', 'y'])
print("numpy→DataFrame:\n", df2)

# ============================================================
# PART 8: 库衔接 —— NumPy ↔ PyTorch
# ============================================================
arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)

# ndarray → Tensor（共享内存！修改一个另一个也变）
tensor = torch.from_numpy(arr)
print("from_numpy:", tensor)          # tensor([1., 2., 3.])

arr[0] = 999.0                        # 修改numpy数组
print("修改arr后tensor:", tensor)     # tensor([999., 2., 3.]) ← tensor也变了！

# Tensor → ndarray（CPU tensor才能直接转，共享内存）
arr_back = tensor.numpy()
print("tensor.numpy():", arr_back)

# GPU tensor 必须先 .cpu() 再转，且不共享内存
# gpu_tensor.cpu().numpy()

# 如果不想共享内存，用 .clone() 先复制
tensor2 = torch.from_numpy(arr.copy())  # 方式1：copy numpy数组
tensor3 = tensor.clone()                # 方式2：clone tensor

# ---- dtype 对应关系 ----
# np.float32  ↔  torch.float32 (torch.FloatTensor)   ← 深度学习最常用
# np.float64  ↔  torch.float64 (torch.DoubleTensor)
# np.int32    ↔  torch.int32
# np.int64    ↔  torch.int64   (torch.LongTensor)    ← 标签/索引常用
# np.bool_    ↔  torch.bool