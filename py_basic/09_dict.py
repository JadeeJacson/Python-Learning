from collections import defaultdict, OrderedDict

def dict_masterclass():
    # 1. 增删改查 (CRUD) 及其防坑指南
    user = {"name": "Alice", "role": "Intern"}
    
    user["age"] = 22             # 增/改: 有则修改，无则新增
    del user["role"]             # 删: 直接删除 (如果 key 不存在会报错 KeyError)
    
    # 查的高阶操作 (实习防崩必写！)
    # print(user["salary"])      # ❌ 极其危险，如果 key 不存在程序直接崩溃
    salary = user.get("salary", 0) # ✅ 优雅：去拿 salary，如果没有，默认返回 0
    print(f"安全查询薪资: {salary}")

    # 2. 遍历三大金刚 (keys, values, items)
    scores = {"Math": 95, "AI": 100}
    # 面试规范：如果你同时需要键和值，永远用 items()，别用 scores[k] 重新去查！
    for subject, score in scores.items(): 
        print(f"科目: {subject}, 分数: {score}")

    score={"jj":100,"cc":150}
    for km,fs in score.items():
        print(f"科目是：{km}分数是：{fs}")
    

    # 3. 字典推导式 (List Comprehension 的亲兄弟)
    # 需求：把所有分数打 8 折
    discounted = {k: v * 0.8 for k, v in scores.items()}
    print(f"打折后的分数: {discounted}")

    # 4. 合并字典：Python 3.9+ 的超级语法糖 (`|` 运算符)
    # 如果有重复的 Key，右边的字典会覆盖左边的！
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 99, "c": 3}
    merged = d1 | d2 
    print(f"合并后的字典: {merged}") # {'a': 1, 'b': 99, 'c': 3}

    # 5. 高阶容器：defaultdict (极其重要！)
    # 统计词频
    employees = [("HR", "Alice"), ("Tech", "Bob"), ("HR", "Charlie"), ("Tech", "David")]
    # 图纸是 list：只要遇到没见过的部门，自动给它建一个空列表 []
    dept_users = defaultdict(list)
    for dept, name in employees:
        # 这一行抵得上普通 dict 的 3 行！直接 append，永不报错
        dept_users[dept].append(name) 
    print("分组结果:", dict(dept_users))# 输出: {'HR': ['Alice', 'Charlie'], 'Tech': ['Bob', 'David']}

    # 6. 高阶容器：OrderedDict (常用于手写 LRU 缓存算法)
    # 注意：Python 3.7 开始，普通 dict 也保证插入顺序了，但 OrderedDict 独有 move_to_end 方法
    od = OrderedDict()
    od["A"] = 1
    od["B"] = 2
    od.move_to_end("A") # 把 A 移到最后面
    print(f"OrderedDict 状态: {list(od.keys())}") # ['B', 'A']

dict_masterclass()



# def hash_under_the_hood():
#     print("=== 1. 见证哈希函数的力量 ===")
#     # 同一个字符串，哈希值绝对相同
#     print(f"hash('AI') = {hash('AI')}")
#     # 稍微改动一点，哈希值天翻地覆
#     print(f"hash('AJ') = {hash('AJ')}")
    
#     print("\n=== 2. 为什么列表不能做 Key？ ===")
#     # 元组是不可变的，算出的哈希值终生不变，所以可以做 Key
#     t = (1, 2)
#     print(f"元组 (1, 2) 的哈希值: {hash(t)}")
    
#     # 列表是可变的。如果允许列表做 Key，今天它的哈希值是 A，放在了 3 号坑。
#     # 明天你给它 append 了一个元素，哈希值变成了 B，你去 3 号坑就再也找不到它了！
#     # 所以 Python 在底层直接封杀：
#     try:
#         lst = [1, 2]
#         hash(lst) 
#     except TypeError as e:
#         print(f"报错了！原因: {e} (列表是不可哈希的)")

#     print("\n=== 3. 字典扩容机制 (模拟) ===")
#     # 字典为了保持 O(1) 的极速，不能让书架装得太满。
#     # Python 字典的装载因子（Load Factor）是 2/3。
#     # 当一个能装 8 个元素的字典，装到第 6 个元素时，Python 就会在底层申请一个 16 个坑位的新书架，把旧数据全部重新哈希搬过去！
#     print("当字典元素超过容量的 2/3 时，会触发底层扩容机制（Rehash）。")

# hash_under_the_hood()