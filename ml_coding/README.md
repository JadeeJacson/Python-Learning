# Machine Learning Coding

这个目录用于把正在学习的机器学习课程转化成独立编码能力。

重点不是保存课程笔记，而是实现课程中的核心算法、训练过程和实验。

## 建议推进顺序

根据课程实际进度逐步添加，例如：

- Linear Regression
- Logistic Regression
- Regularization
- Neural Network
- Model Evaluation
- Decision Tree / Ensemble
- Clustering
- Dimensionality Reduction

不提前为了填满目录创建大量空实现。

## 每个主题建议包含

```text
<topic>/
├── README.md       # 原理、shape、实现思路、实验结论
├── numpy_impl.py   # NumPy 手写核心算法（适用时）
├── sklearn_impl.py # 与成熟库对照（适用时）
├── torch_impl.py   # PyTorch 实现（适用时）
└── test_*.py       # 对关键函数做验证（逐步加入）
```

目录结构按实际需要创建，不要求每个主题机械包含全部文件。

## 实现要求

重点关注：

- 输入输出和矩阵 shape；
- 向量化实现；
- 损失函数；
- 梯度或参数更新；
- 初始化；
- 数值稳定性；
- 训练/验证划分；
- 指标；
- 与成熟库结果对照；
- 最基本的可复现性。

神经网络阶段逐步加入 PyTorch 的标准训练工程结构。

## 与课程学习的关系

默认流程：

```text
课程讲解
→ 数学与机制理解
→ 小规模 NumPy 实现
→ 框架对照
→ 独立练习
→ 工程化改造
```

通过这种方式让机器学习、NumPy、PyTorch 和 Python 工程能力在同一个任务中增长。
