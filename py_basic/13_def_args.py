def ultimate_factory(name, *args, is_vip=False, **kwargs):
    """
    一个集齐了所有参数类型的终极工厂
    - name: 普通位置参数
    - *args: 动态位置参数 (负责接收多余的无名数据)
    - is_vip: 仅关键字参数 (因为在 *args 后面，调用时必须写 is_vip=...)
    - **kwargs: 动态关键字参数 (负责接收多余的带名数据)
    """
    print(f"1. 普通参数 (name): {name}")
    
    # args 在函数内部就是一个纯纯的元组 (Tuple)
    print(f"2. 动态位置参数 (args): {args} -> 类型是 {type(args)}")
    
    print(f"3. 仅关键字参数 (is_vip): {is_vip}")
    
    # kwargs 在函数内部就是一个纯纯的字典 (Dict)
    print(f"4. 动态关键字参数 (kwargs): {kwargs} -> 类型是 {type(kwargs)}")
    print("-" * 30)

# 场景 1：疯狂塞入无名数据
# "Alice" 给了 name，剩下的 "Python", "C++", 99 全被 *args 打包成了元组！
ultimate_factory("Alice", "Python", "C++", 99)

# 场景 2：指名道姓传参与 **kwargs 发威
# "Bob" 给 name；
# "Java" 被 *args 接收；
# is_vip=True 被精确匹配；
# 剩下的 age=25, city="Beijing" 没地方去，全被 **kwargs 打包成了字典！
ultimate_factory("Bob", "Java", is_vip=True, age=25, city="Beijing")