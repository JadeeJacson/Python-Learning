"""
【Python 包结构：__init__.py、绝对导入与相对导入】
请在 VS Code 中运行！
代码会自动在临时沙盒中构建一套逼真的多文件 AI 工程结构，并演示导入过程。
"""
import os
import sys
import tempfile
import shutil

print("="*10, "0. 动态构建 AI 临时工程沙盒", "="*10)
# 创建一个临时文件夹，模拟我们电脑里的真实项目目录
sandbox = tempfile.mkdtemp()
sys.path.insert(0, sandbox) # 告诉 Python 解释器：“去这个沙盒里找我们要的包！”

# 我们要构建的真实目录结构如下：
# my_ai_pkg/
# ├── __init__.py                (集团总前台)
# ├── data/                      (数据部)
# │   ├── __init__.py            (数据部前台)
# │   └── image_loader.py        (干活的模块)
# └── models/                    (算法部)
#     └── neural_net.py          (干活的模块)

pkg_dir = os.path.join(sandbox, "my_ai_pkg")
data_dir = os.path.join(pkg_dir, "data")
models_dir = os.path.join(pkg_dir, "models")
os.makedirs(data_dir); os.makedirs(models_dir)

# a=1: 编写总前台 (my_ai_pkg/__init__.py)
with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
    f.write('print("  [总前台] 欢迎导入 my_ai_pkg，集团基础设施已准备就绪！")\n')

# a=2: 编写底层干活的模块 (image_loader.py)
with open(os.path.join(data_dir, "image_loader.py"), "w", encoding="utf-8") as f:
    f.write('def load(): return ["猫.jpg", "狗.jpg"]\n')

# a=3: 编写数据部前台 (my_ai_pkg/data/__init__.py) -> 演示【相对导入】
with open(os.path.join(data_dir, "__init__.py"), "w", encoding="utf-8") as f:
    f.write('print("  [数据部前台] 正在初始化数据模块...")\n')
    # ⚠️ 相对导入核心：一个点 (.) 代表当前所在目录。
    # 意思是：不要去全网找，就在我同级目录下的 image_loader.py 里把 load 函数拿过来！
    f.write('from .image_loader import load\n') 

# a=4: 编写算法模块 (my_ai_pkg/models/neural_net.py) -> 演示【绝对导入】
with open(os.path.join(models_dir, "neural_net.py"), "w", encoding="utf-8") as f:
    # ⚠️ 绝对导入核心：从集团的根名字 (my_ai_pkg) 开始一级级往下写。
    # 无论这个 neural_net.py 被移动到哪里，这行代码永远能精确找到 load 函数！
    f.write('from my_ai_pkg.data import load\n')
    f.write('def train():\n')
    f.write('    data = load()\n')
    f.write('    print(f"  [算法部] 拿到数据 {data}，开始训练神经网络！")\n')

print("沙盒构建完毕！开始演示 Import 流水线：\n")

# ----------------- 核心导入演示分界线 -----------------

print("="*10, "1. 首次导入集团包", "="*10)
# 这一步会触发 my_ai_pkg/__init__.py 中的 print
import my_ai_pkg 

print("\n"+"="*10, "2. 体验相对导入的便利", "="*10)
# 当我们 import 数据部时，触发了 my_ai_pkg/data/__init__.py。
# 由于该前台已经用相对导入 (from .image_loader import load) 把 load 函数拿到了前台桌面上，
# 所以作为外部调用者的我们，不需要写 my_ai_pkg.data.image_loader.load，
# 而是直接从 data 部门就能拿到 load！(这叫封装内部细节)
from my_ai_pkg.data import load
print(f"在主程序中直接拿到图片: {load()}")

print("\n"+"="*10, "3. 体验绝对导入的稳定性", "="*10)
# 算法部内部使用的是绝对导入去拿数据部的 load。安全、清晰。
from my_ai_pkg.models.neural_net import train
train()

# 打扫战场，删除临时沙盒（工程习惯：不留垃圾）
shutil.rmtree(sandbox)