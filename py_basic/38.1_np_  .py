"""
============================================================
Pandas 基础：
1. 数据结构：Series、DataFrame、Index、dtype、shape、ndim、size
2. 创建数据：pd.Series、pd.DataFrame、pd.read_csv、pd.read_excel、pd.read_json、
             pd.date_range、pd.RangeIndex
3. 读写文件：read_csv、read_excel、read_json、to_csv、to_excel、to_json

适合场景：
数据分析、机器学习数据预处理、日志分析、表格处理、算法工程日常开发

依赖：
pip install pandas openpyxl
============================================================

费曼理解：

如果 NumPy 数组像“纯数字矩阵”，
那么 Pandas 更像“带行号、列名、数据类型的 Excel 表”。

Pandas 主要有两个核心结构：

1. Series：
   一列带索引的数据。
   可以理解为“带名字的列表”。

2. DataFrame：
   多列数据组成的表格。
   可以理解为“Python 里的 Excel 表”。

常见属性：

index：
    行标签，类似 Excel 左边的行号。

dtype：
    一列数据的类型，比如 int64、float64、object、datetime64。

shape：
    表格形状，几行几列。

ndim：
    数据维度。
    Series 是 1 维，DataFrame 是 2 维。

size：
    元素总个数。
    DataFrame 的 size = 行数 * 列数。
"""

import os
import pandas as pd


print("\n==================== 1. Series：一列带索引的数据 ====================")

"""
核心概念：
pd.Series(data) 创建一维数据。

通俗理解：
Series = 一列数据 + 行索引

类似：
下标    值
0      80
1      95
2      88

常见属性：
s.index    # 行索引
s.dtype    # 数据类型
s.shape    # 形状
s.ndim     # 维度
s.size     # 元素个数
"""

scores = pd.Series([80, 95, 88], name="score")

print("scores =")
print(scores)

print("scores.index =", scores.index)
print("scores.dtype =", scores.dtype)
print("scores.shape =", scores.shape)
print("scores.ndim =", scores.ndim)
print("scores.size =", scores.size)

"""
注意：
Series 是一维的。

所以：
shape = (3,)
ndim = 1
size = 3
"""


print("\n==================== 2. Series 自定义 Index ====================")

"""
Index 是行标签。

默认情况下：
index = 0, 1, 2, ...

也可以自己指定。
"""

scores = pd.Series(
    [80, 95, 88],
    index=["小王", "小李", "小张"],
    name="score"
)

print("带自定义索引的 scores =")
print(scores)

print("小李的成绩 =", scores["小李"])

"""
通俗理解：
普通 list 只能用数字下标访问：

lst[0]

Series 可以用有意义的标签访问：

scores["小李"]

这就是 Pandas 比 NumPy 更适合处理表格数据的原因。
"""


print("\n==================== 3. DataFrame：二维表格 ====================")

"""
核心概念：
pd.DataFrame(data) 创建二维表格。

通俗理解：
DataFrame = 多个 Series 拼成的一张表。

每一列可以有自己的 dtype。
这点和 NumPy 不太一样。

NumPy 数组通常要求整体 dtype 更统一；
Pandas 表格可以一列是整数，一列是字符串，一列是日期。
"""

df = pd.DataFrame({
    "name": ["小王", "小李", "小张"],
    "age": [18, 20, 19],
    "score": [80.5, 95.0, 88.5]
})

print("df =")
print(df)

print("df.index =", df.index)
print("df.columns =", df.columns)
print("df.dtypes =")
print(df.dtypes)

print("df.shape =", df.shape)
print("df.ndim =", df.ndim)
print("df.size =", df.size)

"""
解释：
df.shape = (3, 3)
表示 3 行 3 列。

df.ndim = 2
表示 DataFrame 是二维数据。

df.size = 9
表示一共有 3 * 3 = 9 个元素。
"""


print("\n==================== 4. Index：行标签 ====================")

"""
核心概念：
Index 是 Pandas 的行标签。

默认 index 通常是 RangeIndex：
0, 1, 2, 3, ...

你也可以把某一列设置成 index。
"""

df_indexed = df.set_index("name")  # 把 name 列变成行索引

print("df_indexed =")
print(df_indexed)

print("df_indexed.index =", df_indexed.index)

print("查询小李这一行：")
print(df_indexed.loc["小李"])

"""
.loc 是按标签查询。
这里 "小李" 是 index 标签，所以可以用：

df_indexed.loc["小李"]
"""


print("\n==================== 5. dtype：每一列的数据类型 ====================")

"""
核心概念：
dtype 表示数据类型。

常见 dtype：
int64        整数
float64      小数
object       字符串或混合类型
bool         布尔值
datetime64   时间类型

注意：
DataFrame 是多列结构，所以用 df.dtypes 查看每一列 dtype。
Series 是单列结构，所以用 s.dtype。
"""

df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["小王", "小李", "小张"],
    "score": [80.5, 95.0, 88.5],
    "passed": [True, True, True]
})

print("df.dtypes =")
print(df.dtypes)

"""
面试常问：
为什么字符串列 dtype 是 object？

因为 Pandas 早期用 object 来存储 Python 字符串。
现在也有 string dtype，但很多数据读进来仍可能是 object。
"""


print("\n==================== 6. shape、ndim、size 的区别 ====================")

"""
shape：
    看形状，几行几列。

ndim：
    看维度，Series 是 1，DataFrame 是 2。

size：
    看总元素个数。

类比：
shape 像房子的户型：3 行 4 列。
ndim 像房子是平面还是立体。
size 像房间总数量。
"""

s = pd.Series([10, 20, 30])
df = pd.DataFrame({
    "a": [1, 2, 3],
    "b": [4, 5, 6]
})

print("s.shape =", s.shape)
print("s.ndim =", s.ndim)
print("s.size =", s.size)

print("df.shape =", df.shape)
print("df.ndim =", df.ndim)
print("df.size =", df.size)


print("\n==================== 7. pd.Series：创建一列数据 ====================")

"""
常见用法：
pd.Series([1, 2, 3])
pd.Series([1, 2, 3], index=["a", "b", "c"])
pd.Series({"a": 1, "b": 2})

字典创建 Series 时：
key 会变成 index；
value 会变成数据。
"""

s1 = pd.Series([100, 200, 300])
s2 = pd.Series([100, 200, 300], index=["a", "b", "c"])
s3 = pd.Series({"语文": 90, "数学": 95, "英语": 88})

print("s1 =")
print(s1)

print("s2 =")
print(s2)

print("s3 =")
print(s3)


print("\n==================== 8. pd.DataFrame：创建二维表格 ====================")

"""
最常见写法：
用字典创建 DataFrame。

字典的 key 是列名。
字典的 value 是每一列的数据。
"""

students = pd.DataFrame({
    "name": ["小王", "小李", "小张"],
    "age": [18, 20, 19],
    "score": [80, 95, 88]
})

print("students =")
print(students)

"""
也可以用二维列表创建，但要手动指定 columns。
"""

students2 = pd.DataFrame(
    [
        ["小王", 18, 80],
        ["小李", 20, 95],
        ["小张", 19, 88]
    ],
    columns=["name", "age", "score"]
)

print("students2 =")
print(students2)


print("\n==================== 9. pd.date_range：创建时间序列索引 ====================")

"""
核心概念：
pd.date_range 用来创建一串连续日期。

常见用法：
pd.date_range(start="2026-01-01", periods=5)
pd.date_range(start="2026-01-01", end="2026-01-05")
pd.date_range(start="2026-01-01", periods=5, freq="D")

freq 常见值：
D      每天
W      每周
M      每月末
h      每小时
min    每分钟

注意：
新版 Pandas 更推荐小写 h、min。
"""

dates = pd.date_range(start="2026-01-01", periods=5, freq="D")

print("dates =")
print(dates)

sales = pd.DataFrame({
    "date": dates,
    "sales": [100, 120, 90, 150, 130]
})

print("sales =")
print(sales)

"""
真实场景：
时间序列数据，比如：
1. 每天销售额
2. 每小时访问量
3. 每分钟传感器数据
"""


print("\n==================== 10. pd.RangeIndex：创建范围索引 ====================")

"""
核心概念：
pd.RangeIndex 类似 Python 的 range。

常见用法：
pd.RangeIndex(start=0, stop=5, step=1)

它经常作为 DataFrame 的默认索引。
"""

idx = pd.RangeIndex(start=100, stop=105, step=1)

df = pd.DataFrame({
    "score": [80, 95, 88, 76, 90]
}, index=idx)

print("自定义 RangeIndex 的 df =")
print(df)

print("df.index =", df.index)


print("\n==================== 11. read_csv 和 to_csv：读写 CSV 文件 ====================")

"""
CSV 是最常见的数据文件格式之一。
本质上是用逗号分隔的文本表格。

pd.read_csv(filename)：
    读取 CSV 文件为 DataFrame。

df.to_csv(filename)：
    把 DataFrame 保存为 CSV 文件。

常见参数：
index=False      保存时不保存行索引
encoding="utf-8-sig"  方便 Excel 打开中文不乱码
"""

df = pd.DataFrame({
    "name": ["小王", "小李", "小张"],
    "age": [18, 20, 19],
    "score": [80, 95, 88]
})

df.to_csv("students.csv", index=False, encoding="utf-8-sig")

df_from_csv = pd.read_csv("students.csv")

print("从 CSV 读回来的数据 =")
print(df_from_csv)


print("\n==================== 12. read_excel 和 to_excel：读写 Excel 文件 ====================")

"""
Excel 文件常见后缀是 .xlsx。

pd.read_excel(filename)：
    读取 Excel 文件。

df.to_excel(filename)：
    保存为 Excel 文件。

注意：
通常需要安装 openpyxl：
    pip install openpyxl

常见参数：
index=False      保存时不保存行索引
sheet_name       指定工作表名称
"""

df.to_excel("students.xlsx", index=False, sheet_name="学生成绩")

df_from_excel = pd.read_excel("students.xlsx", sheet_name="学生成绩")

print("从 Excel 读回来的数据 =")
print(df_from_excel)


print("\n==================== 13. read_json 和 to_json：读写 JSON 文件 ====================")

"""
JSON 常用于前后端接口、日志、配置文件。

df.to_json(filename)：
    保存为 JSON 文件。

pd.read_json(filename)：
    读取 JSON 文件。

force_ascii=False：
    保存中文时不强制转义，文件更容易看。

orient：
    控制 JSON 的组织方式。
    records 表示每一行是一条记录，工程中常见。
"""

df.to_json("students.json", orient="records", force_ascii=False)

df_from_json = pd.read_json("students.json")

print("从 JSON 读回来的数据 =")
print(df_from_json)


print("\n==================== 14. read_csv 常见参数 ====================")

"""
工程中 read_csv 最常用。

常见参数：

sep：
    分隔符，默认是逗号。
    如果是制表符文件，可以 sep="\\t"。

header：
    哪一行作为列名。
    默认 header=0，表示第一行是列名。

names：
    手动指定列名。

usecols：
    只读取部分列。

dtype：
    指定列的数据类型。

parse_dates：
    把指定列解析成日期。

encoding：
    指定编码，比如 "utf-8"、"gbk"、"utf-8-sig"。
"""

csv_text_df = pd.DataFrame({
    "id": [1, 2, 3],
    "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
    "score": [80, 95, 88]
})

csv_text_df.to_csv("demo.csv", index=False)

demo = pd.read_csv(
    "demo.csv",
    usecols=["id", "date", "score"],    # 只读这些列
    dtype={"id": "int64", "score": "float64"},  # 指定类型
    parse_dates=["date"]                # 把 date 列转成时间类型
)

print("demo =")
print(demo)

print("demo.dtypes =")
print(demo.dtypes)


print("\n==================== 15. 读写后清理临时文件 ====================")

"""
示例代码会生成几个临时文件。
真实项目中不用写这一段。
"""

for filename in [
    "students.csv",
    "students.xlsx",
    "students.json",
    "demo.csv"
]:
    if os.path.exists(filename):
        os.remove(filename)
        print("已删除：", filename)


print("\n==================== 16. 最后总结 ====================")

"""
Series：
    一维带索引数据，像一列 Excel。

DataFrame：
    二维表格，像完整 Excel 表。

Index：
    行标签，不一定只是 0、1、2，也可以是名字、日期等。

dtype：
    数据类型。DataFrame 每一列可以有不同 dtype。

shape：
    数据形状。DataFrame 是 (行数, 列数)。

ndim：
    维度数量。Series 是 1，DataFrame 是 2。

size：
    元素总数。DataFrame 的 size = 行数 * 列数。

pd.Series：
    创建一列数据。

pd.DataFrame：
    创建表格数据。

pd.read_csv / read_excel / read_json：
    从 CSV、Excel、JSON 读取数据。

to_csv / to_excel / to_json：
    把 DataFrame 保存成 CSV、Excel、JSON。

pd.date_range：
    创建连续日期。

pd.RangeIndex：
    创建连续整数索引，常见于默认行索引。
"""