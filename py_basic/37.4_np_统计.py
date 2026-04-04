"""
【NumPy 核心：聚合统计与情报提炼】
请在 VS Code 中运行，特别留意 axis 参数对矩阵形状的“降维压缩”！
"""
import numpy as np

print("="*10, "1. 基础聚合与定向压缩 (axis)", "="*10)
# 假设这是 3 个学生 (行) 的 4 门考试成绩 (列)
scores = np.array([
    [90, 85, 88, 92],
    [70, 75, 78, 80],
    [95, 99, 100, 96]
])
print(f"成绩单矩阵 (3行4列):\n{scores}")

# a=1: 不加 axis，全屏无差别碾压 (计算所有成绩的总平均分)
print(f"\n所有人的总平均分: {scores.mean():.2f}")

# a=2: 垂直压缩 (axis=0) -> 消除行维度，保留列维度
# 把 3 个学生压扁，算出【每门科目】的平均分！
subject_means = scores.mean(axis=0)
print(f"每门科目的平均分 (axis=0): {subject_means} -> shape: {subject_means.shape}")

# a=3: 水平压缩 (axis=1) -> 消除列维度，保留行维度
# 把 4 门科目压扁，算出【每个学生】的总分！
student_sums = scores.sum(axis=1)
print(f"每个学生的总分 (axis=1): {student_sums} -> shape: {student_sums.shape}")


print("\n"+"="*10, "2. 赏金猎人：argmin 与 argmax", "="*10)
# 假设这是 AI 模型输出的对 5 种动物的概率预测
probabilities = np.array([0.05, 0.10, 0.75, 0.08, 0.02])

# max 只知道最大概率是多少
print(f"最大的概率值是: {probabilities.max()}")

# a=4: argmax 找出最大概率在哪个位置 (索引)
# 极其重要！索引 2 代表第 3 种动物，这就是 AI 的最终预测结果！
predicted_class = probabilities.argmax()
print(f"AI 预测的类别索引是 (argmax): {predicted_class}")


print("\n"+"="*10, "3. 滚雪球：cumsum", "="*10)
# a=5: 计算每月的累计营收
monthly_revenue = np.array([100, 150, -50, 200])
# 过程: [100, 100+150, 250-50, 200+200]
print(f"单月营收: {monthly_revenue}")
print(f"累计营收: {monthly_revenue.cumsum()}")


print("\n"+"="*10, "4. 八卦侦探：协方差与相关系数", "="*10)
# a=6: 探索两个变量的关系
# X 是某小区的房屋面积 (平方米)，Y 是对应的房屋价格 (万元)
X = np.array([50, 80, 100, 120, 150])
Y = np.array([100, 155, 205, 230, 310])

# np.corrcoef 会返回一个相关系数矩阵
# 对角线永远是 1.0 (自己和自己 100% 相关)，我们看非对角线的值
corr_matrix = np.corrcoef(X, Y)
print(f"面积与价格的相关系数矩阵:\n{corr_matrix}")
print(f"-> 面积和价格的相关度高达: {corr_matrix[0, 1]:.4f} (极其接近 1，强正相关！)")