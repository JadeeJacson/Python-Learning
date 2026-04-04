def io_demo():
    # 1. input() 的陷阱与转换
    # 注意：在真实的非交互式评测系统里，不要在 input() 里写提示词，会干扰判题
    raw_age = input("请输入你的年龄: ") 
    # 必须手动转换，否则 "20" + 1 会报错
    age = int(raw_age) 
    print(f"明年你 {age + 1} 岁。")

    # 2. print() 的高阶控制
    # sep: 更改多个元素之间的连接符 (默认是空格)
    print("AI", "Intern", "2026", sep="->")  # 输出: AI->Intern->2026
    
    # end: 更改结尾符 (默认是换行 \n)
    print("正在加载", end="")
    print("...", end="")
    print("完成！") # 输出: 正在加载...完成！ (全部在同一行)

    # 3. 文件读写 (核心工程规范：with open)
    # 写入文件 (mode="w" 会覆盖原文件，"a" 是追加)
    file_path = "ai_data.txt"
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write("第一行：自然语言处理\n")
        f.write("第二行：计算机视觉\n")
    # with 代码块结束时，Python 会自动帮你调用 f.close()，即使中间发生了报错！

    # 读取文件
    with open(file_path, mode="r", encoding="utf-8") as f:
        content = f.read()
        print("\n--- 读取的文件内容 ---")
        print(content, end="")

io_demo()

import sys
# 笔试模板：一次性读取所有输入，然后按空格或换行切分
data = sys.stdin.read().split() #这直接从操作系统的标准输入缓冲区抓取数据

#读取大于内存的文件
with open("ai_data.txt", "r") as f:
    for line in f:  # 核心魔法！
        # 处理当前行的内容
        pass