def list_demo():
    # 1. 增 (Add)
    nums = [1, 2, 3]
    nums.append(4)          # 尾部追加: [1, 2, 3, 4]
    nums.insert(0, 99)      # 头部插入: [99, 1, 2, 3, 4] (极其耗时！)
    nums.extend([5, 6])     # 批量拼接: [99, 1, 2, 3, 4, 5, 6]

    # 2. 删 (Delete)
    last_item = nums.pop()  # 弹出尾部: 删掉并返回 6
    first_item = nums.pop(0)# 弹出指定位置: 删掉并返回 99 (极其耗时！)
    nums.remove(3)          # 按值删除: 删掉第一个值为 3 的元素，没有会报错

    # 3. 改与查 (Modify & Query)
    nums[0] = 100           # 改: [100, 2, 4, 5]
    print(f"4 在列表里吗? {4 in nums}") # 查 (返回 True/False)
    
    # 4. 排序与反转
    arr = [3, 1, 4, 1, 5]
    arr.sort()              # 就地排序 (原列表变了): [1, 1, 3, 4, 5]
    arr.reverse()           # 就地反转: [5, 4, 3, 1, 1]
    
    # sorted 返回新列表，原列表不变
    new_arr = sorted([9, 8, 7]) 

    # 5. 列表推导式 (List Comprehension) - 大厂规范：一行顶四行
    # 需求：取出 arr 里的偶数，并求平方
    squares = [x**2 for x in arr if not x & 1 ]
    print(f"偶数平方推导式: {squares}") # [16]

    # 6. 切片拷贝 vs 赋值
    a = [1, 2, 3]
    b = a           # 这叫贴标签！a 和 b 指向同一个列表
    c = a[:]        # 这叫浅拷贝 (Shallow Copy)，切片会生成一个新列表(等于lst.copy())
    b[0] = 999
    print(f"a 被 b 连累了: {a}") # [999, 2, 3]
    print(f"c 安然无恙: {c}")    # [1, 2, 3]

list_demo()


#初始化二维矩阵，防止复制地址
matrix = [[0] * 3 for _ in range(3)]
#_的作用
for _ in range(3): 
        print("我只想重复执行这句话 3 次，数字本身不重要")

def sort_masterclass():
    # 1. 基础认知：sort vs sorted
    nums = [3, 1, 4, 1, 5]
    new_nums = sorted(nums)  # 生成新列表，nums 没变
    nums.sort(reverse=True)  # 原地降序修改 nums
    print(f"原列表被原地修改: {nums}")     # [5, 4, 3, 1, 1]
    print(f"sorted 生成的新列表: {new_nums}") # [1, 1, 3, 4, 5]

    # 2. 进阶：使用 key 和内置函数
    words = ["apple", "hi", "banana", "cat"]
    words.sort(key=len) # 戴上"长度"眼镜，按单词长度排序
    print(f"按长度排序: {words}") # ['hi', 'cat', 'apple', 'banana']

    # 3. 算法核心：用 lambda (匿名函数) 自定义复杂排序规则
    # 假设这是数据库里查出来的员工数据：[姓名, 薪资, 年龄]
    employees = [
        ["Alice", 50000, 25],
        ["Bob", 80000, 30],
        ["Charlie", 50000, 22]
    ]

    # 需求 A：只按薪资 (索引 1) 升序排列
    # lambda x: x[1] 的意思是：我不管你传入的 x（员工列表）长啥样，我只揪出 x[1] 作为排序依据
    employees.sort(key=lambda x: x[1])
    print(f"只按薪资排序: {employees}")

    # 需求 B (大厂机试必考)：多条件组合排序
    # 要求：先按薪资降序，如果薪资相同，再按年龄升序！
    # 语法秘籍：返回一个元组，加负号代表降序
    employees.sort(key=lambda x: (-x[1], x[2]))
    print(f"多条件复杂排序: {employees}") 
    # 结果: Bob先(8万), Charlie第二(5万,22岁), Alice最后(5万,25岁)

sort_masterclass()