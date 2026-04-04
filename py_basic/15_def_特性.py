"""
【Python 函数核心特性:递归、Lambda、高阶函数、流水线三剑客】
请在 VS Code 中运行，并建议在递归函数处打断点，观察左侧的 "Call Stack" (调用栈)
"""
from functools import reduce # reduce 在 Python 3 中被移到了 functools 模块中

print("="*10, "1. 递归 (Recursion)：盗梦空间", "="*10)
# 【核心概念】函数内部调用自己。
# 【底层逻辑】每次调用都会在内存中开辟一个新空间（压栈），
# 直到遇到“终止条件”才开始一层层返回（退栈）。

def calculate_factorial(n, depth=1):
    """计算阶乘 n! = n * (n-1) * ... * 1"""
    indent = "  " * depth # 用于可视化递归深度
    print(f"{indent}向下递进: 正在计算 {n}! (等待 {n-1}! 的结果)")
    
    # ⚠️ 极其重要：递归必须有终止条件（Base Case），否则会无限循环（内存爆栈）
    if n == 1:
        print(f"{indent}>>> 触底反弹: 1! = 1")
        return 1
    
    # 递归调用
    result = n * calculate_factorial(n - 1, depth + 1)
    print(f"{indent}向上回归: {n}! 算出来了，结果是 {result}")
    return result

fact_5 = calculate_factorial(5)
print(f"最终结果: 5! = {fact_5}\n")


print("="*10, "2. Lambda 匿名函数：一次性筷子", "="*10)
# 【核心概念】没有名字的、只有一行的微型函数。语法：lambda 参数: 返回值
# 【底层逻辑】它本质上还是个函数对象，但省去了 def 的繁琐，适合传递给高阶函数使用。

# 实战场景：对包含元组的列表进行排序。比如 (学号, 成绩)
students_scores = [(101, 85), (102, 92), (103, 78)]

# 需求：按成绩（元组的第二个元素）从高到低排序。
# sorted() 的 key 参数需要接收一个函数，这个函数决定了按什么规则排序。
# 这里的 lambda x: x[1] 意思是：
# 对于列表里的每一个元素 x (也就是那个元组)，提取 x[1] 作为排序依据。
sorted_students = sorted(students_scores, key=lambda x: x[1], reverse=True)

print(f"原始数据: {students_scores}")
print(f"按成绩降序: {sorted_students}\n")


print("="*10, "3. 高阶函数 (Higher-order Function)：包工头", "="*10)
# 【核心概念】只要一个函数接收另一个函数作为参数，或者返回一个函数，它就是高阶函数。
# 上面的 sorted() 其实就是内置的高阶函数。我们自己来写一个：

def custom_processor(data_list, action_func):
    """
    这是一个高阶函数。
    data_list: 要处理的列表
    action_func: 具体的处理动作（这也是一个函数！）
    """
    result_list = []
    for item in data_list:
        # 核心：调用外部传进来的函数，具体怎么处理，包工头不关心，工人(action_func)负责
        processed_item = action_func(item) 
        result_list.append(processed_item)
    return result_list

nums = [1, 2, 3]
# 把 lambda 当作参数传进去（让包工头执行“翻倍”的动作）
doubled_nums = custom_processor(nums, lambda x: x * 2)
print(f"原始数组: {nums}")
print(f"使用自定义高阶函数翻倍: {doubled_nums}\n")


print("="*10, "4. Map / Filter / Reduce：流水线三剑客", "="*10)
# 【核心概念】Python 内置的经典高阶函数，专门用于处理可迭代对象（如列表）。

raw_data = [1, 2, 3, 4, 5]
print(f"流水线原料: {raw_data}")

# 4.1 map (加工机)：对列表中的每个元素执行相同的操作
# ⚠️ 坑点：Python 3 中 map 返回的是个“迭代器”(省内存)，
#    必须用 list() 转换才能看到里面的全貌
squared_data = list(map(lambda x: x**2, raw_data))
print(f"Map 加工(求平方): {squared_data}")

# 4.2 filter (筛子)：对列表元素进行判断，只保留返回 True 的元素
even_data = list(filter(lambda x: x % 2 == 0, raw_data))
print(f"Filter 过滤(保留偶数): {even_data}")

# 4.3 reduce (打包机)：对列表元素进行累积操作（比如累加、累乘）
# 执行过程：(((1+2)+3)+4)+5
sum_data = reduce(lambda x, y: x + y, raw_data)
print(f"Reduce 累积(求和): {sum_data}")