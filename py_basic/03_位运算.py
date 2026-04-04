def operator_demo():
    # 1. 算术运算符 (整除与取模),严格的“向下取整”（向负无穷方向）
    print(f"5 除以 2 的普通结果: {5 / 2}")     # 2.5 (永远返回 float)
    print(f"5 除以 2 的向下取整: {5 // 2}")    # 2 (返回 int),严格的“向下取整”（向负无穷方向）
    print(f"5 除以 2 的余数: {5 % 2}")       # 1
    print(f"2 的 3 次方: {2 ** 3}")          # 8

    # 2. 比较运算符 (链式比较 - Python独有特性)
    age = 20
    print(f"年龄是否在 18 到 60 之间: {18 <= age <= 60}") # True (不用写 and)

    # 3. 逻辑运算符 (短路与对象返回)
    default_name = ""
    user_input = "AI_Intern"
    # or 会返回第一个为"真"的【对象】，而不仅仅是 True
    final_name = default_name or user_input 
    print(f"最终用户名: {final_name}") # AI_Intern

    # 4. 位运算 (极其硬核)
    a = 5  # 二进制: 0101
    b = 3  # 二进制: 0011
    print(f"5 & 3 (按位与): {a & b}") # 0001 -> 1
    print(f"5 | 3 (按位或): {a | b}") # 0111 -> 7
    print(f"5 ^ 3 (按位异或): {a ^ b}") # 0110 -> 6

    # 5. 三元运算符 (单行 if-else)
    score = 85
    status = "Pass" if score >= 60 else "Fail"
    print(f"考试状态: {status}")


    # 6. 海象运算符 := (Python 3.8+ 赋值表达式)
    # 允许在表达式内部进行赋值，极大地简化了代码
    if (n := len(user_input)) > 5:
        print(f"用户名太长了，有 {n} 个字符！")

operator_demo()