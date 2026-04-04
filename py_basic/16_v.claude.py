# ============================================================
# Python 闭包：闭包定义 / 自由变量 / nonlocal
# ============================================================


# ────────────────────────────────────────────────────────────
# 第一块：闭包是什么？
# 本质：一个函数"记住"了它被定义时所在环境中的变量
# 类比：你离开家乡，但仍然记得家乡的方言——函数离开了外层作用域，
#       但仍然记得外层的变量
#
# 构成闭包的三个条件：
#   1. 有函数嵌套（内函数定义在外函数内）
#   2. 内函数引用了外函数的变量（自由变量）
#   3. 外函数返回了内函数
# ────────────────────────────────────────────────────────────

print("=== 闭包：最小结构 ===")

def outer():
    msg = "hello"        # ← 这就是"自由变量"：不属于内函数，但被内函数引用

    def inner():
        print(msg)       # inner 引用了外层的 msg

    return inner         # 返回函数本身，不要加括号！加括号是调用

f = outer()              # outer() 执行完毕，正常情况下 msg 应该被销毁
f()                      # 但 msg 依然存在！输出: hello
                         # 因为 inner 持有对 msg 的引用，阻止了它被垃圾回收


# ────────────────────────────────────────────────────────────
# 第二块：自由变量（Free Variable）
# 本质：在函数内部使用，但既不是该函数的参数，也不是局部变量的变量
# Python 把它存在函数的 __closure__ 属性里（cell 对象）
# ────────────────────────────────────────────────────────────

print("\n=== 自由变量：__closure__ 内部存储 ===")

def make_adder(n):
    # n 是 make_adder 的参数，对于内层 adder 来说，n 就是"自由变量"
    def adder(x):
        return x + n     # n 没有在 adder 里定义，它从外层"捕获"
    return adder

add5 = make_adder(5)
add10 = make_adder(10)

print(add5(3))           # 输出: 8    ← add5 记住了 n=5
print(add10(3))          # 输出: 13   ← add10 记住了 n=10

# 查看闭包内部存了什么（调试用，面试能说出来加分）
print(add5.__closure__)                        # (<cell at 0x...>,)
print(add5.__closure__[0].cell_contents)       # 5 ← 就是被捕获的 n


# ────────────────────────────────────────────────────────────
# 第三块：nonlocal 关键字
# 问题背景：在内函数里，直接对自由变量"赋值"会怎样？
# ────────────────────────────────────────────────────────────

print("\n=== 不用 nonlocal：赋值会创建局部变量，不会修改外层 ===")

def make_counter_broken():
    count = 0

    def increment():
        # Python 看到 count = count + 1，认为 count 是局部变量
        # 但局部变量在赋值前就被读取了，所以报错：
        # UnboundLocalError: local variable 'count' referenced before assignment
        count = count + 1   # ← 危险！先读后写，Python 认为是局部变量
        return count

    return increment

# 取消注释可以看到报错：
# f = make_counter_broken()
# f()


print("\n=== 用 nonlocal：声明该变量来自外层，允许修改 ===")

def make_counter():
    count = 0

    def increment():
        nonlocal count       # ← 告诉 Python：count 不是我的局部变量，去外层找
        count = count + 1    # 现在这一行是修改外层的 count，而不是创建新变量
        return count

    return increment

counter = make_counter()
print(counter())   # 输出: 1
print(counter())   # 输出: 2
print(counter())   # 输出: 3   ← 状态被保持了！


# ────────────────────────────────────────────────────────────
# 第四块：global vs nonlocal 的区别
# global：跨越所有层，直接修改模块级全局变量
# nonlocal：只往上找一层（或多层外层函数），不会到达全局
# ────────────────────────────────────────────────────────────

print("\n=== global vs nonlocal 对比 ===")

x = "全局"

def outer():
    x = "外层"

    def inner():
        nonlocal x         # 找到的是 outer 里的 x，不是全局的 x
        x = "被内层修改"

    inner()
    print(x)               # 输出: 被内层修改

outer()
print(x)                   # 输出: 全局 ← 全局的 x 没有被动


# ────────────────────────────────────────────────────────────
# 第五块：经典陷阱——循环中的闭包变量捕获
# 这是面试和刷题中最高频的闭包坑！
# ────────────────────────────────────────────────────────────

print("\n=== 陷阱：循环闭包捕获的是变量引用，不是值 ===")

funcs = []
for i in range(3):
    funcs.append(lambda x: x + i)   # 每个 lambda 都捕获了同一个 i

# 循环结束后 i = 2，所有函数都记住的是同一个 i，此时 i=2
print(funcs[0](0))   # 期望 0，实际输出: 2
print(funcs[1](0))   # 期望 1，实际输出: 2
print(funcs[2](0))   # 期望 2，实际输出: 2


print("\n=== 修复：用默认参数把当前值'快照'固定住 ===")

funcs_fixed = []
for i in range(3):
    # i=i 在函数定义时就把当前 i 的值复制给了默认参数
    # 默认参数是值拷贝，不是引用
    funcs_fixed.append(lambda x, i=i: x + i)

print(funcs_fixed[0](0))   # 输出: 0 ✓
print(funcs_fixed[1](0))   # 输出: 1 ✓
print(funcs_fixed[2](0))   # 输出: 2 ✓


# ────────────────────────────────────────────────────────────
# 实战：用闭包实现带记忆化的函数（算法题加速神器）
# 场景：斐波那契数列，朴素递归 O(2^n) → 闭包缓存 → O(n)
# ────────────────────────────────────────────────────────────

print("\n=== 实战：闭包实现记忆化缓存 ===")

def make_memoized_fib():
    cache = {}               # cache 是自由变量，被内层函数持有

    def fib(n):
        if n in cache:
            return cache[n]  # 命中缓存，直接返回
        if n <= 1:
            return n
        result = fib(n - 1) + fib(n - 2)
        cache[n] = result    # 存入缓存
        return result

    return fib

fib = make_memoized_fib()
print(fib(10))   # 输出: 55
print(fib(35))   # 瞬间输出: 9227465（朴素递归要算几十亿次）