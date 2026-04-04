# ============================================================
# Python 作用域 | LEGB规则 | global & nonlocal
# 费曼核心比喻：Python找变量就像"找人问路"——先问自己(L)，
# 再问外层函数(E)，再查全局地图(G)，最后翻字典(B)
# ============================================================

# ── 1. LEGB 四层查找顺序 ────────────────────────────────────
x = "G_global"          # G: Global 全局

def outer():
    x = "E_enclosing"   # E: Enclosing 外层函数

    def inner():
        x = "L_local"   # L: Local 当前函数
        print(x)        # → "L_local"  命中第一层即停止
    inner()
    print(x)            # → "E_enclosing"

outer()
print(x)                # → "G_global"

# Built-in(B) 示例：len/print 都是内置层，无需导入即可用
print(len([1, 2, 3]))   # len 在 B 层


# ── 2. global：在函数内修改全局变量 ─────────────────────────
# 算法场景：统计递归调用次数
call_count = 0

def dfs(n):
    global call_count   # 声明：我要改的是全局那个
    call_count += 1
    if n == 0:
        return
    dfs(n - 1)

dfs(3)
print(call_count)       # → 4  (3次递推 + 1次base case)

# ⚠️ 不写 global 会怎样？
counter = 10
def bad_modify():
    # counter += 1    # ← UnboundLocalError！
    # Python编译时发现有赋值，就把counter标记为local
    # 但赋值前先读取，local还没值 → 报错
    pass


# ── 3. nonlocal：闭包中修改外层(非全局)变量 ─────────────────
# 工程场景：用闭包实现一个轻量计数器（不用类）
def make_counter():
    count = 0                   # Enclosing 层

    def increment():
        nonlocal count          # 修改外层 count，而非创建新local
        count += 1
        return count

    return increment

counter_a = make_counter()
counter_b = make_counter()      # 独立作用域，互不干扰
print(counter_a())  # → 1
print(counter_a())  # → 2
print(counter_b())  # → 1  ← 独立的 count


# ── 4. 经典陷阱：循环变量捕获（面试高频！）────────────────────
# ❌ 错误写法
funcs_bad = [lambda: i for i in range(3)]
print([f() for f in funcs_bad])   # → [2, 2, 2]  全是2！
# 原因：lambda 捕获的是变量 i 的"引用"，循环结束时 i=2

# ✅ 正确写法：用默认参数把值"冻结"进去
funcs_good = [lambda i=i: i for i in range(3)]
print([f() for f in funcs_good])  # → [0, 1, 2]  ✓


