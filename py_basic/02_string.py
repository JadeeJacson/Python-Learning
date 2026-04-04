def string_demo():
    # 1. 定义：多行字符串与原始字符串
    multiline_str = """这是一个
    多行字符串"""
    
    # 原始字符串 (Raw String): r开头，里面的 \n 不会被当成换行，\t 不会被当成制表符
    # 实习中写正则表达式或 Windows 文件路径时必用！
    path = r"C:\Users\new_intern\test" 
    
    s = "PythonAI"
    # 2. 索引与切片 (重点)
    print(f"第一个字符: {s[0]}")      # P
    print(f"最后一个字符: {s[-1]}")   # I (负索引是Python的一大特色)
    print(f"切片 [0:6]: {s[0:6]}")    # Python (左闭右开区间，包含0不包含6)
    print(f"步长切片 [::2]: {s[::2]}") # PtoA (每隔2个取一个)
    print(f"反转字符串 [::-1]: {s[::-1]}") # IAnohtyP (极其高频的神仙操作)


    # 3. 常用方法 (生成了新字符串，原字符串 s 不变)
    text = "  apple, banana, orange  "

    # strip: 去除两端空白字符（回车、空格、制表符）
    clean_text = text.strip() 
    print(f"strip 去除空格: '{clean_text}'")

    # split: 分割字符串（默认按空白分，这里按逗号分）
    fruits = clean_text.split(",") 
    print(f"split 分割后: {fruits}") # 得到列表: ['apple', ' banana', ' orange']
    
    # join: 拼接字符串（把列表用特定字符连起来）
    joined_text = "-".join(["AI", "Intern", "2026"])
    print(f"join 拼接: {joined_text}") # AI-Intern-2026
    
    s = "PythonAI"
    # replace 与 find (大小写转换)
    print(f"replace 替换: {s.replace('AI', ' Data')}") # Python Data
    print(f"find 查找 'th': {s.find('th')}") # 2 (找不到返回 -1，注意：如果是 index() 找不到会报错)
    print(f"转小写: {s.lower()}") # pythonai

    # 4. 格式化回顾 (三种时代的写法)
    name, score = "Alice", 95
    print("老古董写法: %s 得了 %d 分" % (name, score))
    print("过渡期写法: {} 得了 {} 分".format(name, score))
    print(f"现代规范写法: {name} 得了 {score} 分")

string_demo()