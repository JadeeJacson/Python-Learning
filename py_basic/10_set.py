def set_masterclass():
    print("=== 1. 极速去重与创建防坑 ===")
    raw_data = [1, 2, 2, 3, 3, 3, 4]
    unique_data = list(set(raw_data)) # 大厂最常见的去重写法，一行搞定！
    print(f"列表去重: {unique_data}") # [1, 2, 3, 4]

    # 🛑 致命大坑：创建一个空集合绝对不能用 {} 
    fake_empty_set = {}       # 这是创建了一个空字典！
    real_empty_set = set()    # 这才是空集合！
    
    print("\n=== 2. 数学魔法：交、并、差、补 (圈粉无数的操作) ===")
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    # 交集 (&): 找共同好友
    print(f"交集 (A & B): {a & b}")       # {3, 4}
    
    # 并集 (|): 汇总所有人，自动去重
    print(f"并集 (A | B): {a | b}")       # {1, 2, 3, 4, 5, 6}
    
    # 差集 (-): A 有但 B 没有的 (我有你没有的特长)
    print(f"差集 (A - B): {a - b}")       # {1, 2}
    
    # 对称差集 (^): 只有单方拥有的 (去掉共同好友)
    print(f"对称差集 (A ^ B): {a ^ b}")   # {1, 2, 5, 6}

    print("\n=== 3. 集合推导式 (Set Comprehension) ===")
    # 需求：把下面列表里的单词转大写，并且去重！
    words = ["hello", "world", "hello", "python"]
    unique_upper = {w.upper() for w in words} 
    print(f"集合推导式结果: {unique_upper}") # {'WORLD', 'HELLO', 'PYTHON'} (顺序每次可能不同)

    print("\n=== 4. frozenset:结冰的集合 ===")
    # 普通集合是可变的 (可以 add, remove)
    normal_set = {1, 2}
    normal_set.add(3)
    
    # frozenset 是不可变的，一旦创建，焊死！
    frozen = frozenset([1, 2, 3])
    # frozen.add(4) # ❌ 报错：AttributeError
    print(f"这是一个 frozenset: {frozen}")

set_masterclass()