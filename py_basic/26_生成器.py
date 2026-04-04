"""
【Python 生成器：yield、yield from 与生成器表达式】
请在 VS Code 中运行，并在 sequence_generator 的 yield 处打断点，
体会什么叫做“冻结当前状态并暂停”！
"""
import sys

print("="*10, "1. 生成器表达式：极致的内存魔术", "="*10)
# a=1: 假设我们要处理 100 万个数据
# 传统列表推导式（瞬间在内存中造出 100 万个元素的列表）
list_comp = [x**2 for x in range(1000000)]

# 生成器表达式（仅仅保存了“如何计算平方”的规则，不真正计算）
# 语法区别仅仅是把 [] 换成了 ()
gen_expr = (x**2 for x in range(1000000))

print(f"列表推导式 内存占用: {sys.getsizeof(list_comp)} 字节 (极度耗内存！)")
print(f"生成器表达式 内存占用: {sys.getsizeof(gen_expr)} 字节 (永远只有这么小！)")
# 提取生成器表达式的数据，同样是用 next()
print(f"按需提取第一个值: {next(gen_expr)}\n")


print("="*10, "2. 生成器函数 (yield)：带暂停键的函数", "="*10)
# a=2: 算法题高频场景：斐波那契数列（0, 1, 1, 2, 3, 5...）
# 如果用普通的 return 返回一个列表，当 n 很大时会爆内存。用 yield 完美解决！

def fibonacci_generator(n_max):
    """这是一个生成器函数。只要函数体里有 yield，它就不再是普通函数了。"""
    print("  [底层] 生成器函数启动了！正在初始化变量...")
    a, b = 0, 1
    count = 0
    
    while count < n_max:
        print(f"  [底层] 准备吐出数据: {a} (然后我会暂停在这里！)")
        # ⚠️ 魔法发生的地方：
        # 函数会在这里“交出”变量 a 的值，然后瞬间“冻结”睡眠！
        # 直到外面再次调用 next()，它才会在下一行苏醒，继续往下走。
        yield a 
        
        # 当被唤醒时，从这里继续执行，更新状态
        a, b = b, a + b
        count += 1
        print("  [底层] 我苏醒了，状态已更新，进入下一次循环...")

# 调用生成器函数，【并不会】立即执行函数里面的代码！
# 而是返回一个生成器对象（本质也就是个迭代器）。
fib_gen = fibonacci_generator(3)

print("第一次呼叫 next():")
print(f"拿到的值: {next(fib_gen)}\n")

print("第二次呼叫 next():")
print(f"拿到的值: {next(fib_gen)}\n")


print("="*10, "3. yield from：优雅的嵌套转包", "="*10)
# a=3: 工程实践：将多维嵌套的数据“展平”(Flatten)
nested_data = [[1, 2], [3, 4], [5]]

def flatten_data(nested_list):
    for sublist in nested_list:
        # 传统写法（很啰嗦）：
        # for item in sublist:
        #     yield item
        
        # 优雅的 yield from 写法：
        # 意思是：“从 sublist 这个可迭代对象里挨个要东西，然后直接吐出去”
        yield from sublist

# 借助 for 循环（底层会自动调 iter 和 next）把展平的数据全部取出来
flattened_result = list(flatten_data(nested_data)) #这是函数，所以会直接调用
print(f"嵌套原始数据: {nested_data}")
print(f"展平后的数据: {flattened_result}")