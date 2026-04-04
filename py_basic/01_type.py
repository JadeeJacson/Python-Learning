def type_demo():
    # 1. 基本数据类型定义
    age = 20              # int
    pi = 3.1415           # float
    name = "AI Intern"    # str
    is_ready = True       # bool
    result = None         # NoneType

    # 2. 类型转换 (Explicit Casting)
    age_float = float(age)       # int -> float: 20.0
    pi_int = int(pi)             # float -> int: 3 (向下取整，直接截断)
    is_ready_int = int(is_ready) # bool -> int: 1

    # 3. type() 与 isinstance()
    print(f"age的类型是: {type(age)}") 
    
    # 验证继承关系：bool其实是int的子类
    print(f"is_ready 是 bool 吗? {isinstance(is_ready, bool)}")  # True
    print(f"is_ready 是 int 吗? {isinstance(is_ready, int)}")    # True (因为继承)
    print(f"type判断 is_ready 是 int 吗? {type(is_ready) == int}") # False (严格匹配)

    # 4. None 的判断
    if result is None:
        print("result 目前为空")

type_demo()


#print技巧
user_id = 9527
print(f"{user_id=}") # 输出结果：user_id=9527

pi = 3.1415926
print(f"圆周率大约是: {pi:.2f}")  # 输出: 3.14

uid = 7
print(f"用户编号: {uid:03d}")  # 输出: 007 (总长3位，不够补0)