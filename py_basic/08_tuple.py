from collections import namedtuple

def tuple_masterclass():
    # 1. 元组的创建与单元素陷阱 (高频错误！)
    empty_t = ()
    normal_t = (1, 2, 3)
    # 坑：只放一个元素时，必须加逗号！否则 Python 会认为它只是一个加了括号的普通数学运算
    fake_t = (100)    # 这是一个整数 int 100
    real_t = (100,)   # 这才是一个包含 100 的元组！

    # 2. 绝对不可变性 (但有破绽)
    t = (1, 2, ["A", "B"])
    # t[0] = 99  # ❌ 致命错误：TypeError，防弹玻璃不能打破！
    
    # 魔法破绽：元组本身不可变，但如果里面装了可变的列表，列表里的内容是可以改的！
    t[2].append("C") 
    print(f"看似不可变的元组被修改了: {t}") # 输出: (1, 2, ['A', 'B', 'C'])

    # 3. 极速解包 (Unpacking) - 算法题与解构神器
    # 假设 API 返回了一个坐标和状态
    response = (40.71, -74.00, "Active", "New York")
    
    # 精准解包并丢弃不需要的数据 (结合我们刚学的 _)
    lat, lng, _, city = response
    print(f"解包坐标: {city} ({lat}, {lng})")
    
    # 星号表达式解包 (Python 3 特性)
    first, *middle, last = (10, 20, 30, 40, 50)
    print(f"星号解包中间部分: {middle}") # 自动变成列表: [20, 30, 40]

    # 4. 具名元组 namedtuple (大厂工程规范：数据容器),给元素命名
    # 定义一个叫 Point 的元组类型，它有两个坑位：x 和 y
    Point = namedtuple("Point", ["x", "y"])
    
    p1 = Point(x=10, y=20)
    # 你既可以像老元组一样按索引访问，也可以按高雅的属性名访问！
    print(f"具名元组访问: p1.x={p1.x}, p1[1]={p1[1]}") 
    # p1.x = 99 # ❌ 依然保持不可变性，报错！

tuple_masterclass()