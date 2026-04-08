"""
【Python 封装与访问控制：构建安全的代码黑盒】
请在 VS Code 中运行，并尝试取消注释那些会报错的代码，观察报错信息。
"""

class SmartOptimizer:
    def __init__(self, lr):
        self.public_info = "这是一个 Adam 优化器" # 公有：谁都能看
        self._version = "v1.0"                   # 保护：建议子类使用，外部别碰
        self.__lr = lr                           # 私有：禁止外部直接修改
        self.__iteration_count = 0               # 私有：内部计数，外部不可见

    # ---------------------------------------------------------
    # a=1: 使用 @property 构建 "Getter" (只读接口)
    # ---------------------------------------------------------
    @property
    def learning_rate(self):
        """外界通过 optimizer.learning_rate 获取值，像访问变量一样简单"""
        return self.__lr

    # ---------------------------------------------------------
    # a=2: 使用 @xxx.setter 构建 "Setter" (拦截器/校验器)
    # ---------------------------------------------------------
    @learning_rate.setter
    def learning_rate(self, value):
        """核心业务逻辑：拦截非法参数"""
        if value <= 0:
            # 这里的 raise 能够防止 AI 训练因为非法的学习率而爆炸
            raise ValueError(f"错误：学习率必须大于 0，你输入的是 {value}")
        if value > 1.0:
            print("警告：学习率过大，可能会导致梯度爆炸！")
        
        self.__lr = value
        print(f"成功将学习率更新为: {self.__lr}")

    def step(self):
        """模拟训练一步"""
        self.__iteration_count += 1
        print(f"正在进行第 {self.__iteration_count} 次参数更新...")

# ================= 运行测试 =================

opt = SmartOptimizer(lr=0.01)

# 1. 公有属性：随意访问
print(f"模型信息: {opt.public_info}")

# 2. 私有属性：直接访问会报错
try:
    print(opt.__lr) # ❌ 报错：AttributeError
except AttributeError:
    print("拦截成功：无法直接通过 __lr 访问私有变量")

# 3. 使用 Property 安全访问
print(f"当前学习率 (通过 Property 获取): {opt.learning_rate}")

# 4. 使用 Setter 尝试非法修改
try:
    opt.learning_rate = -0.001 # ❌ 触发拦截逻辑
except ValueError as e:
    print(f"拦截成功: {e}")

# 5. 合法修改
opt.learning_rate = 0.1

# 6. 底层揭秘：Python 的私有属性是真的绝对不可见吗？
# 实际上，Python 只是偷偷改了名字：_类名__变量名
# 这种行为叫 Name Mangling。大厂面试必考！
print(f"强制越权访问私有变量: {opt._SmartOptimizer__lr}")

