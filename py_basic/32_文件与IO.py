"""
【Python 文件与 I/O：文本、二进制、with、CSV、JSON 与 Pickle】
请在 VS Code 中单步调试。运行完毕后，观察左侧目录多出的临时文件！
"""
from pathlib import Path
import csv
import json
import pickle

print("="*10, "0. 准备工作：Pathlib 锁定工作区", "="*10)
# a=1: 使用 pathlib 优雅地定位当前文件夹，并准备好我们要写入的文件名
work_dir = Path.cwd()
text_file = work_dir / "demo_text.txt"
csv_file = work_dir / "demo_data.csv"
json_file = work_dir / "demo_config.json"
pickle_file = work_dir / "demo_model.pkl"


print("\n"+"="*10, "1. 纯文本读写与 with 魔法管家", "="*10)
# a=2: 写入文本文件 (模式 'w' = write，覆盖写入)
# ⚠️ 最佳实践：只要是写文本，永远记得加上 encoding="utf-8"，否则 Windows 默认用 GBK 会导致乱码！
with open(text_file, mode='w', encoding='utf-8') as f:
    f.write("你好，人工智能！\n")
    f.write("这是一条写给未来的测试数据。")
# 只要缩进结束（退出了 with 块），文件 f 就已经被管家自动 close() 了！

# 读取文本文件 (模式 'r' = read)
with open(text_file, mode='r', encoding='utf-8') as f:
    content = f.read()
    print(f"读出的纯文本内容:\n{content}")


print("\n"+"="*10, "2. CSV 表格收纳盒", "="*10)
# a=3: 工程场景：保存算法跑出来的批量数据
ai_records = [
    ["Epoch", "Loss", "Accuracy"],
    [1, 0.85, 0.65],
    [2, 0.42, 0.88]
]

# ⚠️ 坑点：Windows 下写 CSV 必须加 newline=''，否则每行中间会多出一个莫名其妙的空行
with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(ai_records) # 批量写入多行

# 读取 CSV
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    print("读出的 CSV 数据:")
    for row in reader:
        print(f"  -> {row}")


print("\n"+"="*10, "3. JSON 互联网通用翻译盒", "="*10)
# a=4: 工程场景：保存模型的超参数配置
config_dict = {"model": "ResNet", "layers": 50, "use_gpu": True, "tags": ["vision", "ai"]}

with open(json_file, mode='w', encoding='utf-8') as f:
    # json.dump (不带s) 是直接往文件 f 里写；json.dumps (带s) 是转换为 String 字符串
    json.dump(config_dict, f, indent=4, ensure_ascii=False) # indent 让格式漂亮，ensure_ascii 保证中文正常显示

with open(json_file, mode='r', encoding='utf-8') as f:
    loaded_config = json.load(f)
    print(f"读出的 JSON 配置字典: {loaded_config['model']} 模型，{loaded_config['layers']} 层")


print("\n"+"="*10, "4. Pickle：Python 专属二进制冷冻舱", "="*10)
# a=5: 工程场景：我们不仅想存数据，还想存带有方法的“对象实例”！
class MockAIModel:
    def __init__(self, weights):
        self.weights = weights
    def predict(self):
        return f"使用权重 {self.weights} 进行预测！"

my_model = MockAIModel(weights=[0.1, -0.5, 0.8])

# ⚠️ 注意：二进制模式是 'wb' (write binary)。二进制没有字符概念，绝对不要写 encoding 参数！
with open(pickle_file, mode='wb') as f:
    pickle.dump(my_model, f)
    print("[Pickle] AI 模型实例已被液氮冷冻，存入硬盘。")

# 解冻（读取）二进制模式 'rb' (read binary)
with open(pickle_file, mode='rb') as f:
    thawed_model = pickle.load(f)
    print(f"[Pickle] 解冻成功！尝试调用其方法: {thawed_model.predict()}")