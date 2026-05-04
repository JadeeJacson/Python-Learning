# ============================================================
# Pandas 核心入门：数据结构 + 创建数据 + 读写文件
# 建议在 VS Code 中逐块运行，或用 F10 单步调试
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# PART 1：核心数据结构
# ============================================================

# ── Series：一维，带标签的数组（类比：有索引的 list）──────────
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s)
#  a    10
#  b    20
#  c    30
# dtype: int64

print(s['b'])        # 20，通过标签取值
print(s.dtype)       # int64，每列/Series 只有一种类型
print(s.shape)       # (3,)，元组，Series 是一维所以只有一个数
print(s.ndim)        # 1
print(s.size)        # 3，总元素数 = shape 所有维度相乘

# ── DataFrame：二维表格（类比：Excel 表 / SQL 表）────────────
data = {
    'name':  ['Alice', 'Bob', 'Charlie'],
    'score': [88, 95, 70],
    'pass':  [True, True, False]
}
df = pd.DataFrame(data)
print(df)
#       name  score   pass
# 0    Alice     88   True
# 1      Bob     95   True
# 2  Charlie     70  False

print(df.shape)   # (3, 3)  → (行数, 列数)
print(df.ndim)    # 2，DataFrame 永远是二维
print(df.size)    # 9 = 3行 × 3列，总格子数
print(df.dtypes)  # 每列各自的 dtype（注意是 dtypes 复数！）

# ── Index：行标签对象（不是普通 list！）──────────────────────
print(df.index)           # RangeIndex(start=0, stop=3, step=1)
print(df.columns)         # Index(['name', 'score', 'pass'], dtype='object')

# RangeIndex：懒加载的范围索引，不真正占内存（类比 Python 的 range）
ri = pd.RangeIndex(start=0, stop=5, step=1)
print(ri)                 # RangeIndex(start=0, stop=5, step=1)
print(list(ri))           # [0, 1, 2, 3, 4]，转成 list 才会展开

# ── dtype 速查 ────────────────────────────────────────────────
# int64    → 整数
# float64  → 浮点
# object   → 字符串或混合类型（底层是 Python 对象，操作慢！）
# bool     → 布尔
# datetime64[ns] → 时间（ns = 纳秒精度）
# category → 枚举类型，适合重复值多的列，节省内存

# ============================================================
# PART 2：创建数据
# ============================================================

# ── pd.Series 四种常见创建方式 ───────────────────────────────
s1 = pd.Series([1, 2, 3])                          # 从 list
s2 = pd.Series({'x': 1, 'y': 2})                   # 从 dict，key 自动成 index
s3 = pd.Series(np.array([4.0, 5.0, 6.0]))          # 从 ndarray
s4 = pd.Series(0, index=['a', 'b', 'c'])            # 广播：全部填 0
print(s4)  # a 0 / b 0 / c 0

# ── pd.DataFrame 三种常见创建方式 ────────────────────────────
# 方式1：dict of list（最常用）
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

# 方式2：list of dict（每行是一个 dict，适合动态拼接结果）
df2 = pd.DataFrame([{'A': 1, 'B': 3}, {'A': 2, 'B': 4}])

# 方式3：二维 ndarray + 指定列名
df3 = pd.DataFrame(np.arange(6).reshape(2, 3), columns=['x', 'y', 'z'])
print(df3)
#    x  y  z
# 0  0  1  2
# 1  3  4  5

# ── pd.date_range：生成时间序列索引 ──────────────────────────
dates = pd.date_range(start='2024-01-01', periods=5, freq='D')  # freq='D' 每天
print(dates)
# DatetimeIndex(['2024-01-01', '2024-01-02', ..., '2024-01-05'], dtype='datetime64[ns]', freq='D')

# 常用 freq：'D'=天, 'h'=小时, 'ME'=月末, 'YE'=年末
df_ts = pd.DataFrame({'value': [10, 20, 15, 30, 25]}, index=dates)
print(df_ts)

# ============================================================
# PART 3：读写文件（重点：参数！）
# ============================================================

# ── 先造一个测试 CSV ──────────────────────────────────────────
df_origin = pd.DataFrame({
    'id':    [1, 2, 3],
    'name':  ['Alice', 'Bob', 'Charlie'],
    'score': [88.5, 95.0, 70.3]
})
df_origin.to_csv('test.csv', index=False)  # index=False：不把行号写进文件！
# 如果不写 index=False，CSV 第一列会多出 0,1,2 的行号列 ← 新手常见坑

# ── read_csv 重点参数 ─────────────────────────────────────────
df_csv = pd.read_csv(
    'test.csv',
    # header=0,          # 默认第0行为列名；header=None 表示无列名
    # usecols=['id','score'],  # 只读指定列，大文件必备，节省内存
    # dtype={'id': int, 'score': float},  # 显式指定列类型，避免自动推断错误
    # na_values=['N/A', '-'],  # 把这些字符串也识别为 NaN
    # encoding='utf-8',  # 中文 CSV 有时需要 'gbk' 或 'utf-8-sig'
)
print(df_csv)
print(df_csv.dtypes)

# ── to_csv 重点参数 ───────────────────────────────────────────
df_csv.to_csv(
    'output.csv',
    index=False,          # 几乎每次都要加！
    # encoding='utf-8-sig', # 输出给 Excel 打开时加这个，否则中文乱码
    # columns=['id','name'], # 只输出指定列
    # sep='\t',             # 改成制表符分隔（TSV 格式）
)

# ── read_excel / to_excel ─────────────────────────────────────
# 需要安装：pip install openpyxl
df_origin.to_excel('test.xlsx', index=False, sheet_name='Sheet1')
df_xl = pd.read_excel(
    'test.xlsx',
    sheet_name='Sheet1',  # 也可以传数字 0 表示第一个 sheet
    # usecols='A:C',      # Excel 风格列范围
)
print(df_xl)

# ── read_json / to_json ───────────────────────────────────────
df_origin.to_json('test.json', orient='records', indent=2)
# orient='records' → 输出格式：[{"id":1,"name":"Alice",...}, ...]
# 其他 orient：'split','index','columns','values','table'

df_js = pd.read_json('test.json', orient='records')
print(df_js)

# ── 小结对比表（用 print 模拟）───────────────────────────────
print("""
格式        读取函数          写入函数        常用必填参数
CSV         read_csv          to_csv          index=False
Excel       read_excel        to_excel        sheet_name, index=False（需 openpyxl）
JSON        read_json         to_json         orient='records'
""")