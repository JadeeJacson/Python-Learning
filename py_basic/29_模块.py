"""
【Python 模块与包：import 体系与 __main__ 的终极奥义】
请在 VS Code 中运行。观察最后一部分的 if __name__ == '__main__': 是如何工作的！
"""

# a=1: 全量导入 (搬来整个箱子)
import math 
# a=2: 局部导入并起别名 (只拿需要的工具，并改个短名字)
from datetime import datetime as dt
# a=3: 导入子模块/类，这是 AI 框架中最常见的写法
from collections import defaultdict

print("="*10, "1. 命名空间与别名的实战", "="*10)
# 因为是 import math，所以必须带上箱子的名字
print(f"调用 math 箱子里的工具: {math.ceil(3.14)}") 

# 因为起了别名 dt，直接用 dt 即可
current_time = dt.now().strftime("%Y-%m-%d")
print(f"当前时间 (使用别名 dt): {current_time}")


print("\n"+"="*10, "2. 模拟一个 AI 核心算法模块", "="*10)

def calculate_model_loss(predictions, targets):
    """
    模拟一个计算 AI 模型误差的函数。
    假设这个文件叫做 ai_metrics.py。
    在实际工程中，这个函数会被其他文件 import 过去使用。
    """
    if len(predictions) != len(targets):
        raise ValueError("预测值和真实值长度不一致！")
    
    # 使用了 defaultdict 这个外来工具
    error_stats = defaultdict(float)
    total_error = 0.0
    
    for p, t in zip(predictions, targets):
        error_stats['abs_diff'] += abs(p - t)
        total_error += abs(p - t)
        
    return total_error / len(predictions)

# ----------------- 核心分界线 -----------------

# a=4: 基因检测仪 (Guest vs Host)
# 为什么所有的专业 Python 脚本最后都要加这句话？
# 假设当前这个文件叫 ai_metrics.py：
# - 如果你在这个文件里点击“运行”，__name__ 就是 '__main__'，下面的测试代码会执行。
# - 如果明天你在 main.py 里写了 `import ai_metrics`，这个文件会被悄悄跑一遍，
#   但是此时它的 __name__ 是 'ai_metrics'，不等于 '__main__'，
#   所以下面的测试代码【绝对不会】被执行，防止了“一导入就自动跑测试”的尴尬灾难！

if __name__ == '__main__':
    print("\n"+"="*10, "3. 模块自测试区 (只有直接运行时才会触发)", "="*10)
    print(f"当前文件的真实身份标识 __name__ 是: '{__name__}'")
    print("因为身份是 __main__，确认是主人自己运行，开始执行内部单元测试...")
    
    # 构造假数据进行测试
    mock_preds = [0.9, 0.2, 0.8]
    mock_targets = [1.0, 0.0, 1.0]
    
    loss = calculate_model_loss(mock_preds, mock_targets)
    print(f"测试完成，当前算法算出的模型平均误差为: {loss:.4f}")
    print("[成功] 模块测试通过，可以放心让别人 import 了！")