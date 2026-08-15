# Python-Learning

这个仓库用于持续巩固 Python、学习 C++ 进阶内容，并把编程训练与机器学习课程、算法和工程实践结合起来。

当前原则：**保留已有学习内容，不为了目录整洁大规模迁移旧文件；新增内容按新的学习架构继续积累。**

## 现有内容

- `py_basic/`：此前的 Python 基础与进阶学习代码，包含容器、函数、闭包、装饰器、面向对象、并发、NumPy 等内容。继续保留原位置，主要用于复习和查漏补缺。
- `py_algo/`：此前的 Python 算法练习。继续保留原位置。

## 新增学习主线

```text
Python-Learning/
├── py_basic/              # 已有 Python 学习代码，保留不迁移
├── py_algo/               # 已有 Python 算法代码，保留不迁移
├── python_engineering/    # Python 工程能力
├── scientific_python/     # NumPy / 线性代数 / Pandas / sklearn / PyTorch
├── cpp/                   # C++ 复习、进阶与底层机制
├── cpp_algo/              # 用 C++ 重做典型算法题
├── ml_coding/             # 机器学习算法手写与框架实现
├── mini_projects/         # 小型综合项目
├── templates/             # 学习模板
└── LEARNING_GUIDE.md      # 学习方式与推进规则
```

## 当前学习定位

### Python：主线

不从变量、`if`、`for` 重新完整学一遍，而采用“复习 + 查漏补缺 + 工程化”的方式。

优先复习容易遗忘的部分：

- 函数参数、作用域、闭包、装饰器
- 面向对象、继承、抽象、dataclass
- 迭代器、生成器、上下文管理
- 异常处理
- 多线程、多进程、asyncio
- 类型标注

随后重点转向：

- 项目结构与模块化
- 环境与依赖管理
- logging / config / pathlib
- pytest
- API 与数据处理
- 可维护的 AI/ML 工程代码

### Scientific Python / 机器学习：主线

和当前机器学习课程同步推进：

- NumPy：复习已有内容并补齐 broadcasting、索引、向量化、随机数、线性代数等
- 矩阵与线性代数：把数学概念和 NumPy 代码对应起来
- Pandas / Matplotlib：数据分析与实验可视化
- scikit-learn：标准机器学习工作流
- PyTorch：Tensor、autograd、nn.Module、Dataset/DataLoader、训练循环、GPU

机器学习知识尽量经历：

1. 数学与算法理解
2. NumPy 手写
3. scikit-learn 对照
4. PyTorch 实现（适用时）

### C++：支线

基础语法已学习过，因此不重新完整入门。先快速恢复，再重点学习：

- 引用、指针、const、栈与堆
- 对象生命周期、RAII
- STL 与迭代器
- 智能指针
- 拷贝 / 移动语义
- 继承、多态与虚函数
- 模板
- Modern C++ 常用特性
- CMake、调试与基本工程结构

C++ 同时作为算法题的第二实现语言，为以后可能涉及的 AI Infra / 推理 / 系统方向打基础。

## 每个知识点怎么学

统一采用五阶段模板：

1. **Concept**：概念、机制、适用场景、常见误区、工程意义。
2. **Demo**：一份精简、可运行、重点明确的教学代码。
3. **Practice**：从空文件独立实现，AI 不直接给完整答案。
4. **Engineering**：把知识点放进真实的小模块、ML 代码或项目中。
5. **Check**：确认能解释、能独立写、能实际使用。

详细规则见 [`LEARNING_GUIDE.md`](./LEARNING_GUIDE.md)。

## 近期推进顺序

1. Python 能力诊断与高级语法快速恢复。
2. NumPy + 线性代数系统复习，并与机器学习课程同步。
3. Python 工程基础逐步加入现有 ML 练习。
4. PyTorch 系统学习。
5. C++ 作为支线持续推进，并用典型算法题练 STL 与语言能力。
6. 用 `ml_coding/` 和 `mini_projects/` 把知识转化为可展示、可解释的代码能力。

这个仓库的目标不是收集尽可能多的笔记，而是逐步形成能够独立编写、调试、解释和工程化代码的能力。
