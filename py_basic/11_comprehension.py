def comprehension_masterclass():
    # 假设这是我们从网页爬虫抓取到的原始脏数据
    raw_data = ["  apple ", "BANANA", "  ", "cherry", "APPLE"]

    # 1. 列表推导式 (List Comprehension): 清洗并转小写
    # 逻辑: 只要不是纯空格的词 (if d.strip())，就把两端去空格并转小写 (d.strip().lower())
    clean_list = [d.strip().lower() for d in raw_data if d.strip()] # 纯空格->0
    print(f"列表推导: {clean_list}") 
    # ['apple', 'banana', 'cherry', 'apple']

    # 2. 集合推导式 (Set Comprehension): 清洗并自动去重
    # 只是把外面的 [] 换成了 {}
    clean_set = {d.strip().lower() for d in raw_data if d.strip()}
    print(f"集合推导 (去重): {clean_set}") 
    # {'cherry', 'banana', 'apple'}

    # 3. 字典推导式 (Dict Comprehension): 建立单词到长度的映射
    # 必须有冒号！比如 'apple': 5
    word_len_dict = {word: len(word) for word in clean_set}
    print(f"字典推导: {word_len_dict}") 
    # {'cherry': 6, 'banana': 6, 'apple': 5}

    # 4. 生成器表达式 (Generator Expression): 神奇的圆括号 ()
    # 注意：它不会立刻执行，而是返回一个 generator 对象！
    gen = (len(d) for d in raw_data)
    print(f"\n生成器本身: {gen}") # <generator object ...>
    
    # 怎么用图纸？用 next() 催它，或者扔进 for 循环里
    print(f"按需生产第一个: {next(gen)}") # 8 (也就是 "  apple " 的长度)
    print(f"按需生产第二个: {next(gen)}") # 6 (也就是 "BANANA" 的长度)

comprehension_masterclass()