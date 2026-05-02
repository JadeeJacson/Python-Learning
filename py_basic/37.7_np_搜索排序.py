# ============================================================
# 排序 & 搜索 完整讲解
# sort / argsort / unique / searchsorted / argpartition
# ============================================================
import numpy as np

np.random.seed(42)

# ============================================================
# PART 1: sort —— 排序
# ============================================================
# 【两种用法，行为完全不同，是最常见的踩坑点！】

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# 用法1：np.sort(arr) → 返回新数组，原数组不变
sorted_arr = np.sort(arr)
print("np.sort 结果:", sorted_arr)   # [1 1 2 3 4 5 6 9]
print("原数组不变:  ", arr)           # [3 1 4 1 5 9 2 6]

# 用法2：arr.sort() → 原地修改，返回None（和shuffle一样的坑！）
arr_copy = arr.copy()
arr_copy.sort()                       # 直接修改 arr_copy
print("原地sort结果:", arr_copy)      # [1 1 2 3 4 5 6 9]

# 降序：np.sort 没有直接参数，用[::-1]翻转
desc = np.sort(arr)[::-1]
print("降序:       ", desc)           # [9 6 5 4 3 2 1 1]

# ---- 二维数组排序（面试常考）----
mat = np.array([[3, 1, 2],
                [6, 4, 5]])

print("按列排序(axis=0):\n", np.sort(mat, axis=0))  # 每列内部排序
# [[3 1 2]
#  [6 4 5]]

print("按行排序(axis=1):\n", np.sort(mat, axis=1))  # 每行内部排序
# [[1 2 3]
#  [4 5 6]]

# ============================================================
# PART 2: argsort —— 返回排序后的索引（非常重要！）
# ============================================================
# 【核心用途】不直接排值，而是告诉你"排完序后，原来哪个位置的元素在这里"
# 算法题中用于：按某列排序、获取TopK索引、间接排序多个数组

scores = np.array([85, 92, 78, 95, 88])
names  = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve']

idx = np.argsort(scores)           # 返回升序排列的索引
print("升序索引:", idx)             # [2 0 4 1 3] ← 78,85,88,92,95对应的原始位置

# 用索引去取值（间接排序）
print("按成绩升序排名:", np.array(names)[idx])   # ['Charlie' 'Alice' 'Eve' 'Bob' 'Dave']
print("对应分数验证: ", scores[idx])              # [78 85 88 92 95]

# 降序：argsort 后翻转
idx_desc = np.argsort(scores)[::-1]
print("按成绩降序排名:", np.array(names)[idx_desc])  # ['Dave' 'Bob' 'Eve' 'Alice' 'Charlie']

# ---- 实战：获取Top-K的索引 ----
# 取分数最高的3人（先argsort降序，再取前3）
top3_idx = np.argsort(scores)[::-1][:3]
print("Top3:", np.array(names)[top3_idx], scores[top3_idx])  # Dave Bob Eve / 95 92 88

# ============================================================
# PART 3: unique —— 去重 + 附带统计信息
# ============================================================
# np.unique(ar, return_index, return_inverse, return_counts)

data = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])

# 基本用法：仅去重，结果自动升序
u = np.unique(data)
print("去重结果:", u)               # [1 2 3 4 5 6 9]

# return_counts=True：同时返回每个值出现的次数（词频统计场景）
u, counts = np.unique(data, return_counts=True)
print("元素:", u)                   # [1 2 3 4 5 6 9]
print("次数:", counts)              # [2 1 2 1 3 1 1]

# 找出现次数最多的元素（众数）
print("众数:", u[np.argmax(counts)])  # 5（出现3次）

# return_index=True：返回每个唯一值第一次出现的位置
u, first_idx = np.unique(data, return_index=True)
print("首次出现位置:", first_idx)

# return_inverse=True：返回原数组每个元素在unique结果中的下标（可还原原数组）
u, inverse = np.unique(data, return_inverse=True)
print("inverse索引:", inverse)
print("用inverse还原:", u[inverse])  # 和原data完全一样

# ============================================================
# PART 4: searchsorted —— 二分查找插入位置（O(log n)）
# ============================================================
# 【前提】数组必须是有序的！
# 返回"插入该值后仍保持有序"的位置索引

sorted_data = np.array([10, 20, 30, 40, 50])

# side='left'（默认）：返回最左可插入位置
pos_left  = np.searchsorted(sorted_data, 25, side='left')
print("left  插入25的位置:", pos_left)   # 2（插在30前面）

# side='right'：返回最右可插入位置（存在重复值时有区别）
pos_right = np.searchsorted(sorted_data, 30, side='right')
print("right 插入30的位置:", pos_right)  # 3（插在已有30的右边）

# ---- left vs right 区别（重复值场景）----
arr_dup = np.array([1, 2, 2, 2, 3])
print("left  插入2:", np.searchsorted(arr_dup, 2, side='left'))   # 1
print("right 插入2:", np.searchsorted(arr_dup, 2, side='right'))  # 4

# ---- 实战：判断元素是否存在于有序数组 ----
def exists_in_sorted(arr, val):
    idx = np.searchsorted(arr, val)
    return idx < len(arr) and arr[idx] == val   # 检查位置上的值是否真的等于val

print("30是否存在:", exists_in_sorted(sorted_data, 30))  # True
print("25是否存在:", exists_in_sorted(sorted_data, 25))  # False

# ---- 批量查询（传入数组）----
targets = np.array([15, 30, 45])
positions = np.searchsorted(sorted_data, targets)
print("批量插入位置:", positions)   # [1 2 4]

# ============================================================
# PART 5: argpartition —— O(n) 快速TopK，不完全排序
# ============================================================
# 【核心思想】只保证第k小的元素在正确位置，其左边都比它小，右边都比它大
# 比完全排序 O(n log n) 快，当只需要TopK时优先用这个！

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])

# 找最小的3个元素（k=3，取前3）
k = 3
part_idx = np.argpartition(arr, k)      # 前k个位置放的都是最小的k个元素
smallest3_idx = part_idx[:k]           # 取前k个索引
smallest3 = arr[smallest3_idx]
print("最小3个元素(无序):", smallest3)   # 如 [1 1 2]，顺序不保证

# 如果需要有序的TopK，再对这k个排一次序
sorted_smallest3 = np.sort(arr[smallest3_idx])
print("最小3个元素(有序):", sorted_smallest3)  # [1 1 2]

# 找最大的3个元素（k=-3，取后3）
largest3_idx = np.argpartition(arr, -k)[-k:]
print("最大3个元素(无序):", arr[largest3_idx])   # 如 [9 6 5]
print("最大3个元素(有序):", np.sort(arr[largest3_idx])[::-1])  # [9 6 5]

# ---- sort vs argpartition 性能对比（大数据量时差异明显）----
big = np.random.rand(1_000_000)

import time

t0 = time.time()
np.sort(big)[-100:]           # 完全排序取Top100
print(f"sort    耗时: {time.time()-t0:.4f}s")  # 约 0.08s

t0 = time.time()
idx = np.argpartition(big, -100)[-100:]  # 只做部分排序
big[idx]
print(f"argpart 耗时: {time.time()-t0:.4f}s")  # 约 0.01s，快约8倍