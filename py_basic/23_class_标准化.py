"""
【Python 架构双壁：强制契约(ABC)与智能容器(Dataclass)】
请在 VS Code 中运行，注意观察由于“没签契约”导致的强硬报错！
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

print("="*10, "1. 抽象基类 (ABC)：大厂接口防呆设计", "="*10)

# a=1: 继承 ABC，说明这是一个“图纸/契约”，它自己不能被实例化！
class BaseAIModel(ABC):
    
    @abstractmethod
    def forward(self, x):
        """强制契约：所有的子类模型，必须实现 forward 前向传播方法！"""
        pass
        
    @abstractmethod
    def compute_loss(self):
        """强制契约：所有的子类模型，必须实现算 loss 的方法！"""
        pass

# ❌ 错误示范：叛逆的子类（忘记实现 compute_loss）
class BadModel(BaseAIModel):
    def forward(self, x):
        return x * 2

try:
    # a=2: 见证 ABC 的绝对防御！在实例化这一刻就会直接爆炸，不让你带病上线。
    bad_ai = BadModel() 
except TypeError as e:
    print(f"[ABC 拦截成功] 无法开业：{e}")

# ✅ 正确示范：听话的子类（实现了所有抽象方法）
class GoodModel(BaseAIModel):
    def forward(self, x):
        return x * 2
        
    def compute_loss(self):
        return 0.05

good_ai = GoodModel()
print("[ABC 通过] 听话的子类成功实例化！")


print("\n"+"="*10, "2. 数据类 (Dataclass)：极其清爽的配置管理", "="*10)

# a=3: @dataclass 魔法贴纸。注意我们甚至可以用类型提示 (Type Hinting)
@dataclass
class TrainingConfig:
    model_name: str
    learning_rate: float
    batch_size: int = 32 # 可以设置默认值
    
    # a=4: 💣 究极避坑点！如果你要给列表/字典这种可变对象设默认值，绝对不能写 tags: list = []
    # 必须用 field(default_factory=...)，否则所有实例会共享同一个列表！
    hidden_layers: List[int] = field(default_factory=lambda: [64, 128])

# 自动拥有了完美的 __init__
config1 = TrainingConfig(model_name="ResNet", learning_rate=0.001)

# a=5: 自动拥有了极其漂亮的 __repr__ (打印出来的样子)
print(f"训练配置详情:\n{config1}")

# a=6: 自动拥有了 __eq__ (判断两个对象里面的值是否相等)
config2 = TrainingConfig(model_name="ResNet", learning_rate=0.001)
print(f"config1 和 config2 数据相等吗？ -> {config1 == config2}") 
# (如果不用 dataclass，普通的类直接 == 比较的是内存地址，会返回 False！)