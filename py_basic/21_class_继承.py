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


print("\n"+"="*10, "2. 多继承与 MRO (方法解析顺序)", "="*10)

# 定义两个有冲突的父类
class TextEncoder:
    def encode(self):
        print("[TextEncoder] 提取文本特征")
    
    def status(self):
        print("状态: 文本模块正常")

class ImageEncoder:
    def encode(self):
        print("[ImageEncoder] 提取图像特征")
        
    def status(self):
        print("状态: 图像模块正常")

# a=3: 多继承混血儿。注意括号里的顺序！(TextEncoder 在前)
class MultiModalModel(TextEncoder, ImageEncoder):
    def encode_all(self):
        print("[MultiModalModel] 开始多模态融合...")
        # 这个类自己没有 encode() 和 status()，它会去父类里找
        self.encode() 
        self.status()

multimodal = MultiModalModel()
print("-" * 20)
multimodal.encode_all() 
# 思考：它到底调用的是 Text 的还是 Image 的？
# 答案：按照 MRO！

print("\n[揭秘 MRO 族谱顺位]")
# a=4: 查看 Python 底层为你排好的继承顺序
# 规则是从左到右，深度优先，但在多继承钻石结构中遵循 C3 算法
for cls in MultiModalModel.mro():
    print(f" -> {cls.__name__}")