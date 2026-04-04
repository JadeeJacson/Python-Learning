"""
【Python 元编程魔法：__slots__、描述符、__new__ 与 Metaclass】
请在 VS Code 中运行。这部分代码略度烧脑，请重点阅读注释与打印输出的顺序！
"""

print("="*10, "1. 极致省内存的 __slots__", "="*10)

class NormalPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    # a=1: 锁死对象的属性。它将不再有 __dict__，无法动态添加新属性！
    __slots__ = ['x', 'y'] 
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = NormalPoint(1, 2)
p2 = SlottedPoint(1, 2)

p1.z = 3  # 正常对象：随心所欲动态添加属性
print(f"正常对象 p1 拥有动态字典: {p1.__dict__}")

try:
    p2.z = 3  # 企图给 slotted 对象添加不在名单里的属性
except AttributeError as e:
    print(f"[拦截] Slotted 对象报错了: {e} (因为节省了内存，牺牲了自由)")


print("\n"+"="*10, "2. 描述符 (Descriptor) - 属性的私人保安", "="*10)

# a=2: 只要一个类实现了 __get__ 和 __set__，它就是一个描述符
class ValidatedAge:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        # instance 是拥有这个属性的对象 (比如下面的 user)
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} 必须是整数！")
        if value < 0 or value > 150:
            raise ValueError(f"{self.name} 必须在 0-150 之间！")
        print(f"[保安放行] 成功将 {self.name} 设置为 {value}")
        instance.__dict__[self.name] = value

class User:
    # 把描述符实例化，作为类的类属性
    age = ValidatedAge("age")

user = User()
user.age = 25  # 触发 __set__
try:
    user.age = -10 # 触发 __set__ 并被拦截
except ValueError as e:
    print(f"[描述符拦截报错]: {e}")


print("\n"+"="*10, "3. __new__ - 拦截对象的诞生 (单例模式)", "="*10)

class DatabaseConnection:
    _instance = None # 记录是否已经建过房子了

    # a=3: __new__ 是真正的构造器，它负责“返回一个内存实例”
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("[建筑工人 __new__] 发现还没盖过房子，正在分配内存打地基...")
            # 调用父类 (object) 的 __new__ 真正开辟内存
            cls._instance = super().__new__(cls)
        else:
            print("[建筑工人 __new__] 发现房子已经存在了，直接把旧钥匙交出去！")
        return cls._instance

    # a=4: 无论 __new__ 是新建还是复用，__init__ 都会被执行去“软装”
    def __init__(self):
        print("[软装设计师 __init__] 正在初始化数据库连接参数...\n")

db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(f"这两个数据库连接是同一个内存对象吗？ {db1 is db2}")


print("\n"+"="*10, "4. 元类 (Metaclass) - 拦截类的诞生", "="*10)

# a=5: 定义一个 3D 打印机 (继承自 type)。
# 它的任务是：强制要求被它制造出来的所有“类”，其内部的方法名必须全大写！
class StrictMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        print(f"[元类发力] 正在检查类 '{name}' 的蓝图...")
        new_attrs = {}
        for attr_name, attr_value in attrs.items():
            # 跳过魔法方法 (如 __init__)
            if not attr_name.startswith('__') and callable(attr_value):
                # 把方法名强行转成大写
                new_attrs[attr_name.upper()] = attr_value
            else:
                new_attrs[attr_name] = attr_value
                
        # 拿着修改后的蓝图，去真正创建这个类
        return super().__new__(mcs, name, bases, new_attrs)

# a=6: 使用 metaclass= 指派这台 3D 打印机来造这个类
class APIClient(metaclass=StrictMetaclass):
    def fetch_data(self):
        return "获取到了远端数据！"

# 见证奇迹：原来的 fetch_data 找不到了，被元类强行改成了 FETCH_DATA！
client = APIClient()
print(f"调用被元类篡改的方法: {client.FETCH_DATA()}")