"""
============================================================
NumPy 进阶基础：
1. 内存布局：copy、view、stride、contiguous、C order、F order
2. IO 操作：save、load、savez、savetxt、loadtxt
3. 库衔接：tolist、to_numpy、values、from_numpy

适合场景：
算法刷题、机器学习数据处理、NumPy/Pandas/PyTorch 衔接、工程开发
============================================================

费曼理解：

NumPy 数组不是简单的“二维列表”。

它更像是：
    一块连续或不连续的内存 + 一套解释这块内存的规则。

这套规则包括：
1. shape：数组长什么形状
2. dtype：每个元素是什么类型
3. strides：走到下一个元素要跨多少字节
4. order：内存里按行放，还是按列放
5. copy/view：到底是复制了一份数据，还是共用同一块数据

这些知识很重要，因为它直接影响：
1. 程序是否改到了原数据
2. 代码是否省内存
3. 运行速度是否快
4. 和 Pandas、PyTorch 衔接时是否安全
"""

import os
import numpy as np


print("\n==================== 1. copy：真正复制一份数据 ====================")

"""
核心概念：
arr.copy() 会创建一份新数据。

通俗理解：
copy 就像复印一份试卷。
你改复印件，不会影响原件。
"""

arr = np.array([1, 2, 3, 4])
arr_copy = arr.copy()

arr_copy[0] = 999

print("原数组 arr =", arr)
print("复制数组 arr_copy =", arr_copy)

"""
底层逻辑：
arr 和 arr_copy 是两块不同内存。
所以修改 arr_copy 不会影响 arr。
"""

print("arr_copy 是否和 arr 共享内存：", np.shares_memory(arr, arr_copy))


print("\n==================== 2. view：共享同一块数据，只是换个视角 ====================")

"""
核心概念：
view 不复制底层数据。
它只是用新的 shape、strides 等信息重新解释同一块内存。

通俗理解：
view 不是复印试卷，而是用不同角度看同一张试卷。
你在 view 上改内容，原数组也会变。
"""

arr = np.array([1, 2, 3, 4])
arr_view = arr[1:3]  # 切片通常返回 view，不是 copy

arr_view[0] = 999

print("arr_view =", arr_view)
print("原数组 arr =", arr)

"""
为什么 arr[1] 变了？
因为 arr_view 和 arr 共用同一块底层内存。
arr_view[0] 对应的就是 arr[1]。
"""

print("arr_view 是否和 arr 共享内存：", np.shares_memory(arr, arr_view))


print("\n==================== 3. copy 和 view 的核心区别 ====================")

"""
一句话区别：

copy：
    新开一块内存，互不影响。

view：
    共用一块内存，修改一方可能影响另一方。

工程经验：
如果你只是读数据，用 view 省内存。
如果你要修改数据，又不希望影响原数组，用 copy。
"""

arr = np.array([10, 20, 30, 40])

a = arr[1:3]        # view
b = arr[1:3].copy() # copy

a[0] = 200
b[1] = 300

print("arr =", arr)
print("a view =", a)
print("b copy =", b)


print("\n==================== 4. stride：数组在内存里怎么走 ====================")

"""
核心概念：
arr.strides 表示：
沿着每个维度移动 1 步，需要跨多少字节。

注意：
strides 的单位是“字节”，不是元素个数。

比如 int64 占 8 字节。
"""

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
], dtype=np.int64)

print("A =\n", A)
print("A.shape =", A.shape)
print("A.dtype =", A.dtype)
print("A.itemsize =", A.itemsize, "字节")
print("A.strides =", A.strides)

"""
A.shape = (2, 3)
A.strides 可能是 (24, 8)

意思是：
1. 从 A[0][0] 到 A[1][0]，也就是下一行，要跨 24 字节
2. 从 A[0][0] 到 A[0][1]，也就是下一列，要跨 8 字节

为什么下一行是 24 字节？
因为一行有 3 个 int64：
3 * 8 = 24 字节
"""


print("\n==================== 5. 转置为什么通常不复制数据？ ====================")

"""
A.T 是转置。
很多时候 A.T 不复制数据，只是改变 strides。

原来按行看：
A =
[[1, 2, 3],
 [4, 5, 6]]

转置后按列看：
A.T =
[[1, 4],
 [2, 5],
 [3, 6]]

底层数据可能还是同一块，只是走路规则变了。
"""

B = A.T

print("B = A.T =\n", B)
print("A.strides =", A.strides)
print("B.strides =", B.strides)
print("B 是否和 A 共享内存：", np.shares_memory(A, B))

B[0, 1] = 999  # B[0, 1] 对应 A[1, 0]

print("修改 B 后 A =\n", A)

"""
重点：
转置常常是 view。
所以修改转置后的数组，可能会影响原数组。
"""


print("\n==================== 6. contiguous：内存是否连续 ====================")

"""
核心概念：
contiguous 表示数组在内存里是不是连续排放的。

C_CONTIGUOUS：
    是否是 C order 连续，也就是按行连续。

F_CONTIGUOUS：
    是否是 Fortran order 连续，也就是按列连续。

为什么重要？
因为很多底层库希望数组是连续内存。
连续内存通常访问更快，也更方便传给 C/C++/PyTorch 等库。
"""

C = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

T = C.T

print("C.flags =")
print(C.flags)

print("T = C.T")
print("T.flags =")
print(T.flags)

"""
你通常会看到：
C 是 C_CONTIGUOUS=True
T 可能不是 C_CONTIGUOUS

因为 T 只是换了 strides，不一定重新排内存。
"""


print("\n==================== 7. np.ascontiguousarray：变成 C 连续内存 ====================")

"""
核心概念：
np.ascontiguousarray(arr) 会确保 arr 是 C order 连续的。

如果 arr 本来就是 C 连续：
    可能不复制。

如果 arr 不是 C 连续：
    会复制一份连续内存。

常用于：
1. 传给底层 C/C++ 库
2. 传给某些机器学习框架
3. 避免因为非连续内存导致性能下降或报错
"""

T_contig = np.ascontiguousarray(T)

print("T 是否 C 连续：", T.flags["C_CONTIGUOUS"])
print("T_contig 是否 C 连续：", T_contig.flags["C_CONTIGUOUS"])
print("T_contig 是否和 T 共享内存：", np.shares_memory(T, T_contig))


print("\n==================== 8. C order 和 F order ====================")

"""
C order：
    按行优先存储。
    一行一行放进内存。
    Python/NumPy 默认更常见。

F order：
    按列优先存储。
    一列一列放进内存。
    Fortran、某些科学计算库常见。

举例：
矩阵：
[[1, 2, 3],
 [4, 5, 6]]

C order 内存顺序：
[1, 2, 3, 4, 5, 6]

F order 内存顺序：
[1, 4, 2, 5, 3, 6]
"""

A_c = np.array([[1, 2, 3], [4, 5, 6]], order="C")
A_f = np.array([[1, 2, 3], [4, 5, 6]], order="F")

print("A_c =\n", A_c)
print("A_c.ravel(order='C') =", A_c.ravel(order="C"))
print("A_c.flags['C_CONTIGUOUS'] =", A_c.flags["C_CONTIGUOUS"])

print("A_f =\n", A_f)
print("A_f.ravel(order='F') =", A_f.ravel(order="F"))
print("A_f.flags['F_CONTIGUOUS'] =", A_f.flags["F_CONTIGUOUS"])


print("\n==================== 9. IO：np.save 和 np.load ====================")

"""
核心概念：
np.save(filename, arr)：
    把单个 NumPy 数组保存成 .npy 文件。

np.load(filename)：
    从 .npy 文件读取数组。

特点：
1. 保留 dtype
2. 保留 shape
3. 适合 NumPy 内部高效读写
4. 比 txt 更适合保存数组
"""

arr = np.array([[1, 2, 3], [4, 5, 6]])

np.save("demo_arr.npy", arr)

loaded_arr = np.load("demo_arr.npy")

print("loaded_arr =\n", loaded_arr)
print("loaded_arr.dtype =", loaded_arr.dtype)
print("loaded_arr.shape =", loaded_arr.shape)


print("\n==================== 10. IO：np.savez 保存多个数组 ====================")

"""
核心概念：
np.savez(filename, a=arr1, b=arr2)
可以把多个数组保存到一个 .npz 文件里。

通俗理解：
.npy 是一个数组一个文件。
.npz 是多个数组打包成一个压缩包式文件。
"""

x = np.array([1, 2, 3])
y = np.array([[10, 20], [30, 40]])

np.savez("demo_multi.npz", x=x, y=y)

data = np.load("demo_multi.npz")

print("npz 里面有哪些名字：", data.files)
print("data['x'] =", data["x"])
print("data['y'] =\n", data["y"])

data.close()  # 工程习惯：用完关闭


print("\n==================== 11. IO：savetxt 和 loadtxt ====================")

"""
核心概念：
np.savetxt(filename, arr)：
    把数组保存成文本文件，比如 .txt 或 .csv。

np.loadtxt(filename)：
    从文本文件读取数组。

特点：
1. 人类可读
2. 适合和其他工具交换简单数据
3. 但不如 .npy 高效
4. 对复杂 dtype、对象数组、多维数组不友好
"""

scores = np.array([
    [1, 80],
    [2, 95],
    [3, 88]
], dtype=float)

np.savetxt("scores.csv", scores, delimiter=",", fmt="%.1f")

loaded_scores = np.loadtxt("scores.csv", delimiter=",")

print("loaded_scores =\n", loaded_scores)

"""
delimiter=","：
    表示用逗号分隔，类似 CSV。

fmt="%.1f"：
    表示保存时保留 1 位小数。
"""


print("\n==================== 12. 库衔接：tolist ====================")

"""
核心概念：
arr.tolist() 把 NumPy 数组转成 Python 原生 list。

什么时候用？
1. 要把数据返回给接口 JSON
2. 某些库只接受 Python list
3. 调试时想看得更普通

注意：
转成 list 后，就不再是 NumPy 数组了。
没有 shape、dtype、向量化计算能力。
"""

arr = np.array([[1, 2, 3], [4, 5, 6]])

lst = arr.tolist()

print("arr 类型：", type(arr))
print("lst 类型：", type(lst))
print("lst =", lst)


print("\n==================== 13. Pandas 衔接：to_numpy 和 values ====================")

"""
这部分需要 pandas。
如果你还没装：
    pip install pandas

df.to_numpy()：
    Pandas 官方更推荐的方式，把 DataFrame 转成 NumPy 数组。

df.values：
    也能取到底层数组，但不如 to_numpy 语义清晰。
"""

try:
    import pandas as pd

    df = pd.DataFrame({
        "age": [18, 20, 22],
        "score": [80, 95, 88]
    })

    arr1 = df.to_numpy()
    arr2 = df.values

    print("df =\n", df)
    print("df.to_numpy() =\n", arr1)
    print("df.values =\n", arr2)

    """
    推荐：
        df.to_numpy()

    原因：
        语义更明确：我要把 Pandas 数据转成 NumPy。
    """

except ImportError:
    print("当前环境没有安装 pandas，跳过 pandas 示例。")


print("\n==================== 14. PyTorch 衔接：from_numpy ====================")

"""
这部分需要 torch。
如果你还没装：
    pip install torch

torch.from_numpy(arr)：
    把 NumPy 数组转成 PyTorch Tensor。

关键点：
    from_numpy 通常共享内存。

也就是说：
    改 NumPy 数组，Tensor 可能跟着变。
    改 Tensor，NumPy 数组也可能跟着变。

这是面试和工程里的高频坑。
"""

try:
    import torch

    arr = np.array([1, 2, 3], dtype=np.float32)

    t = torch.from_numpy(arr)

    print("arr =", arr)
    print("t =", t)

    arr[0] = 999

    print("修改 arr 后：")
    print("arr =", arr)
    print("t =", t)

    t[1] = 888

    print("修改 tensor 后：")
    print("arr =", arr)
    print("t =", t)

    """
    如果不想共享内存，可以 clone 一份：
        t_safe = torch.from_numpy(arr).clone()
    """

    t_safe = torch.from_numpy(arr).clone()

    arr[2] = 777

    print("clone 后再修改 arr：")
    print("arr =", arr)
    print("t_safe =", t_safe)

except ImportError:
    print("当前环境没有安装 torch，跳过 PyTorch 示例。")


print("\n==================== 15. 清理本示例生成的文件 ====================")

"""
工程习惯：
示例代码生成的临时文件，用完可以删除。
"""

for filename in ["demo_arr.npy", "demo_multi.npz", "scores.csv"]:
    if os.path.exists(filename):
        os.remove(filename)
        print("已删除：", filename)


print("\n==================== 16. 最后总结 ====================")

"""
copy：
    真复制，新内存，改副本不影响原数组。

view：
    不复制，共享内存，改 view 可能影响原数组。

stride：
    表示每个维度走一步跨多少字节。

contiguous：
    表示内存是否连续，影响性能和库衔接。

C order：
    行优先存储，NumPy 默认常见。

F order：
    列优先存储，科学计算和 Fortran 常见。

save/load：
    保存和读取单个 .npy 数组。

savez：
    一个 .npz 文件保存多个数组。

savetxt/loadtxt：
    文本格式保存和读取，适合简单可读数据。

tolist：
    NumPy 转 Python list。

to_numpy：
    Pandas 转 NumPy，推荐写法。

values：
    Pandas 旧式取底层数据方式，不如 to_numpy 清晰。

from_numpy：
    NumPy 转 PyTorch Tensor，通常共享内存。
"""