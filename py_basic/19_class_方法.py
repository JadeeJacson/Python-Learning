"""
【Python 方法类型：实例方法、类方法、静态方法】
请在 VS Code 中运行。重点观察这三种方法是如何被调用的（用类名调还是用实例调）。
"""

class AIDataset:
    """模拟一个 AI 数据集管理类（兵工厂）"""
    
    # 【类变量】兵工厂的公共资产：记录总共加载了多少个数据集
    total_datasets_loaded = 0
    
    def __init__(self, name, data_list):
        # 【实例变量】具体数据集的私有资产
        self.name = name
        self.data = data_list
        # 每造出一个数据集实例，工厂的统计就加 1
        AIDataset.total_datasets_loaded += 1

    print("="*10, "1. 实例方法：机器人的专属技能", "="*10)
    # 【底层逻辑】必须有 self。只有具体的实例才能调用，用来操作实例自己的数据。
    def get_data_summary(self):
        """实例方法：汇报当前数据集的情况"""
        # 必须通过 self 访问自己的名字和数据
        count = len(self.data)
        print(f"[实例方法执行] 数据集 '{self.name}' 包含 {count} 条数据。")
        return count


    print("="*10, "2. 类方法 (@classmethod)：厂长的特殊制造工艺", "="*10)
    # 【底层逻辑】必须有 cls。通常用于两件事：1. 修改类变量 2. 提供"备用构造函数"（最常见！）
    @classmethod
    def from_csv_string(cls, csv_string):
        """
        类方法：备用构造函数。
        假设我们拿到的是一个逗号分隔的字符串，而不是列表。
        我们让"厂长"来处理这个字符串，并直接返回一个造好的新实例！
        """
        print("[类方法执行] 厂长收到特殊材料，正在转换...")
        # 把字符串切分成列表
        parsed_data = csv_string.split(',')
        
        # ⚠️ 核心：cls() 就相当于 AIDataset()。
        # 这样做的好处是，如果以后这个类改名了，或者被继承了，代码不用改！
        new_dataset_instance = cls(name="CSV导入数据集", data_list=parsed_data)
        return new_dataset_instance


    print("="*10, "3. 静态方法 (@staticmethod)：保安/外包工具人", "="*10)
    # 【底层逻辑】既不需要 self 也不需要 cls。它就是一个普通的函数，只是恰好写在了类里面。
    @staticmethod
    def validate_data_type(data):
        """
        静态方法：仅仅用来做个校验。
        它不关心是哪个数据集(无 self)，也不关心工厂状态(无 cls)。
        """
        print("[静态方法执行] 保安正在检查数据格式...")
        if isinstance(data, list):
            print("  -> 校验通过：是合法的列表格式。")
            return True
        else:
            print("  -> 校验失败：数据必须是列表！")
            return False


# ================== 实战调用演示 ==================

print("\n--- A. 测试实例方法 ---")
# 1. 先得用标准图纸（__init__）造一个实例出来
my_dataset = AIDataset("图像分类训练集", ["img1.jpg", "img2.jpg", "img3.jpg"])
# 2. 用实例对象调用实例方法
my_dataset.get_data_summary() 


print("\n--- B. 测试类方法 (备用构造) ---")
# ⚠️ 注意：这里我们不需要先造实例！直接用【类名】调用厂长的方法
raw_string = "text1,text2,text3,text4"
# 厂长干完活，直接返回了一个新造出来的实例！
csv_dataset = AIDataset.from_csv_string(raw_string) 
csv_dataset.get_data_summary() # 验证一下造出来的实例能不能正常工作


print("\n--- C. 测试静态方法 ---")
# ⚠️ 注意：也是直接用【类名】调用。把它当成一个收纳在类里的普通工具函数就行。
AIDataset.validate_data_type(["a", "b", "c"])
AIDataset.validate_data_type("这段文字不是列表")

print(f"\n[全局通知] 工厂目前总共造了 {AIDataset.total_datasets_loaded} 个数据集。")