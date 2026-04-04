# 1. 函数定义：建厂图纸
# name, base_salary 是普通参数；bonus 带有默认值，是默认参数
def calculate_salary(name, base_salary, bonus=0):
    """
    这是一个计算员工最终薪资的函数 (这叫 Docstring,大厂强制要求的文档注释)
    """
    total = base_salary + bonus
    
    # 2. 返回值：把算好的结果运出去。如果想返回多个值，可以用逗号隔开 (其实是打包成了元组)
    return total, f"{name}的最终薪资是: {total}"

print("=== 1. 位置参数 (严格按顺序匹配) ===")
# "Alice" 给 name，10000 给 base_salary，2000 给 bonus
num1, msg1 = calculate_salary("Alice", 10000, 2000)
print(msg1) 

print("\n=== 2. 关键字参数 (无视顺序，指名道姓) ===")
# 只要指明了参数名，顺序可以随便打乱！极大地提高了代码可读性
num2, msg2 = calculate_salary(bonus=5000, name="Bob", base_salary=20000)
print(msg2)

print("\n=== 3. 默认参数 (不传就不按，传了就覆盖) ===")
# 我只传了前两个，第三个 bonus 我没传，工厂自动使用了默认值 0
num3, msg3 = calculate_salary("Charlie", 8000)
print(msg3)