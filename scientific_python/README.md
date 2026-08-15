# Scientific Python & PyTorch

这个目录用于把 Python 数值计算能力与机器学习课程同步推进。

## 第一阶段：NumPy + 矩阵复习与补齐

优先内容：

- ndarray / dtype / shape / axis
- 索引、切片、布尔索引
- reshape / transpose / squeeze / concatenate
- broadcasting
- 向量化与减少 Python `for` 循环
- 聚合统计
- 随机数与可复现性
- 矩阵乘法、点积、范数
- 线性方程组
- 特征值 / 特征向量、SVD 的代码对应
- 数值稳定性与浮点精度的基本概念

已经在 `py_basic/` 学过的 NumPy 文件不迁移；这里用于后续更系统的复习、练习以及机器学习关联实现。

## 第二阶段：数据与实验工具

- Pandas：表格数据、缺失值、筛选、分组、合并
- Matplotlib：训练曲线、决策边界、数据分布等基础可视化
- scikit-learn：数据拆分、预处理、模型训练、评估、Pipeline

## 第三阶段：PyTorch

建议顺序：

1. Tensor 与 NumPy 对照
2. shape / broadcasting / indexing
3. device 与 dtype
4. autograd
5. `nn.Module`
6. 常见 loss 与 optimizer
7. Dataset / DataLoader
8. 标准 training loop / validation loop
9. checkpoint
10. GPU 基础
11. 调试梯度、shape 和数值问题

## 学习方式

对于机器学习课程中出现的重要算法，尽量完成：

```text
数学原理
→ NumPy 手写核心过程
→ scikit-learn 对照
→ PyTorch 实现（适用时）
```

尤其关注矩阵 shape、向量化、损失函数、梯度与训练数据流，而不是只记库函数名称。
