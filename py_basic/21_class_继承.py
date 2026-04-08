"""
【Python 面向对象：继承体系与 MRO 魔法】
请在 VS Code 中单步调试，观察子类是如何调用父类方法以及解决冲突的。
"""

print("="*10, "1. 单继承、重写与 super()", "="*10)

# 1. 定义祖传基类 (父类)
class BaseModel:
    def __init__(self, name):
        self.name = name
        self.weights_loaded = False
        print(f"[BaseModel] 初始化基础模型: {self.name}")

    def forward(self, x):
        print("[BaseModel] 默认前向传播：直接原样返回")
        return x
        
    def save_weights(self):
        print(f"[BaseModel] 正在保存 {self.name} 的权重到硬盘...")

# 2. 定义子类 (单继承)
class ResNet(BaseModel):
    def __init__(self, name, layers):
        # a=1: 核心！使用 super() 呼叫父类的初始化方法，帮我们把 name 和基础属性绑定好
        # 如果不写这句，子类会丢失父类的基因 (比如 self.weights_loaded 会不存在，直接报错)
        super().__init__(name) 
        self.layers = layers
        print(f"[ResNet] 初始化子类属性，层数: {self.layers}")

    # a=2: 方法重写 (Override)
    def forward(self, x):
        print(f"[ResNet] 正在执行 {self.layers} 层的残差网络前向传播...")
        # 有时候我们也想在重写中利用父类逻辑，依然可以呼叫 super()
        # super().forward(x) 
        return x * 2

# 测试单继承
my_model = ResNet(name="ResNet-50", layers=50)
print("-" * 20)
my_model.save_weights() # 儿子没有写，但继承了老爸的家产，直接用！
my_model.forward(10)    # 儿子重写了，所以执行儿子自己的前向传播逻辑



print("="*10, "菱形继承战场：爷爷、大伯、二伯与你", "="*10)

# A：共同的最顶层基类 (爷爷)
class GrandBase:
    def __init__(self):
        print("[GrandBase] 爷爷被初始化了！(最底层的基因)")
        self.health = 100

# B：左侧父类 (大伯)
class LeftParent(GrandBase):
    def __init__(self):
        # a=1: 这里的 super() 会去哪？在单继承里它是找 GrandBase。
        # 但在菱形继承里，它的下一个目标其实是 RightParent！这就是 C3 算法的魔力。
        super().__init__()
        print("[LeftParent] 大伯被初始化了！注入《太极·刚》基因")
        self.attack = 80

# C：右侧父类 (二伯)
class RightParent(GrandBase):
    def __init__(self):
        # a=2: 这里的 super() 才会真正去找 GrandBase 爷爷。
        super().__init__()
        print("[RightParent] 二伯被初始化了！注入《太极·柔》基因")
        self.defense = 80

# D：你 (混血儿，同时继承大伯和二伯)
# a=3: 注意这里的顺序，Left 在前，Right 在后
class Child(LeftParent, RightParent):
    def __init__(self):
        # a=4: 开始击鼓传花！呼叫 MRO 链条的下一个
        super().__init__()
        print("[Child] 你被初始化了！集齐所有基因，天下无敌！")

# ================= 见证奇迹的时刻 =================

print("\n【1. 查看 C3 算法生成的绝对族谱 (MRO)】")
# 打印 MRO 列表。这就是 Python 底层 C3 算法算出来的优先级！
mro_list = Child.mro()
for i, cls in enumerate(mro_list):
    print(f"顺位 {i}: {cls.__name__}")
# 预期输出: Child -> LeftParent -> RightParent -> GrandBase -> object


print("\n【2. 实例化对象，触发击鼓传花】")
# a=5: 请在这里打断点！单步调试进入 __init__
# 执行路径将会是：Child -> LeftParent -> RightParent -> GrandBase
# 打印出来的顺序刚好是【反向】的，因为大家都在等超类的 __init__ 执行完毕再执行自己的 print！
my_hero = Child()

print("\n【3. 检查最终状态】")
print(f"你的属性: 生命 {my_hero.health}, 攻击 {my_hero.attack}, 防御 {my_hero.defense}")