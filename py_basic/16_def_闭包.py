"""
【Python 闭包核心特性:闭包定义、自由变量、nonlocal】
请在 VS Code 中运行，并在 averager 函数内部打断点，观察调试器左侧 Variables 面板中的 "Closure" (闭包) 变量。
"""

print("="*10, "1. 闭包与自由变量：带记忆的函数", "="*10)
# 实战场景：我们需要记录一个AI模型在多个Epoch（轮次）下的平均Loss值。
# 不想使用全局变量（污染环境），此时闭包是最好的选择。

def make_loss_averager():
    """外层函数：负责提供环境和背包"""
    # 这里的 history_losses 对于内层函数来说，就是【自由变量】
    # 它存在于外层函数中，即将被内层函数“打包”带走
    history_losses = [] 
    
    def averager(new_loss):
        """内层函数：真正的执行者"""
        # ⚠️ 注意：这里我们修改了 history_losses (用了 append)
        # 为什么不需要 nonlocal？因为 list 是可变对象，我们是在“修改”它的内容，而不是把它“重新赋值”为一个新列表。
        history_losses.append(new_loss)
        current_avg = sum(history_losses) / len(history_losses)
        print(f"[Debug] 当前背包里的历史 Loss: {history_losses}")
        return current_avg
    
    # 关键点：返回内层函数本身（不加括号！），让它带着 history_losses 这个背包去流浪
    return averager 

# 创建一个闭包实例
# 此时 make_loss_averager 已经执行完毕被销毁，但它里面的 history_losses 活下来了！
track_loss = make_loss_averager()

# 验证闭包的记忆功能
avg1 = track_loss(0.8)
print(f"第一次输入 Loss 0.8，当前平均值: {avg1}\n")

avg2 = track_loss(0.6)
print(f"第二次输入 Loss 0.6，当前平均值: {avg2}\n")


print("="*10, "2. nonlocal 的作用：修改不可变的自由变量", "="*10)
# 上面的例子每次都要用 sum()，时间复杂度 O(N)，很慢。
# 算法题优化：我们只存“当前总和(total)”和“数量(count)”就行了，空间 O(1)！

def make_optimized_averager():
    total = 0.0  # 自由变量：数字（不可变对象）
    count = 0    # 自由变量：数字（不可变对象）
    
    def averager(new_loss):
        # 💣 致命错误警告：如果不加下面这行，直接写 count += 1 会报错：
        # "UnboundLocalError: local variable 'count' referenced before assignment"
        # 因为 Python 认为 count += 1 相当于 count = count + 1，这是在创建一个新的【局部变量】，从而屏蔽了外面的自由变量。
        
        # ✅ 解决方案：申请修改许可证
        nonlocal total, count 
        
        count += 1
        total += new_loss
        print(f"[Debug] nonlocal 生效，当前总和: {total}, 次数: {count}")
        return total / count
        
    return averager

opt_track_loss = make_optimized_averager()
print(f"优化版第一次平均值: {opt_track_loss(0.8)}")
print(f"优化版第二次平均值: {opt_track_loss(0.6)}")

# 查看闭包底层的秘密（验证机制）
print("\n[窥探底层] 这个函数究竟带了什么背包？")
print(f"闭包变量内容: {[cell.cell_contents for cell in opt_track_loss.__closure__]}")


"""说说你对闭包的理解？它和面向对象（类）有什么区别？
你的回答： 
闭包是一个绑定了外部作用域变量的函数。它是封装数据的一种轻量级方式。
区别在于： 面向对象（类）是“附带各种方法的数据”（以数据为核心，方法服务于数据）；
而闭包是“附带数据的函数”（以行为为核心，数据服务于行为）。
在只需要一两个方法时，写闭包比写一个完整的类更简洁、优雅。"""