def matrix_chain_order(p):
    """
    p: 维度数组，长度为 n+1，表示 n 个矩阵
       A_i 的维度为 p[i-1] x p[i]（1-indexed）
    返回: m（最小代价表）, s（分割点记录表）
    """
    n = len(p) - 1  # 矩阵数量
    
    # m[i][j]: A_i..A_j 的最小乘法次数（1-indexed，用0-indexed实现）
    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]  # 记录最优分割点
    
    # l 是子链长度
    for l in range(2, n + 1):          # 长度从 2 开始
        for i in range(n - l + 1):     # 起点 i（0-indexed）
            j = i + l - 1              # 终点 j
            m[i][j] = float('inf')
            
            for k in range(i, j):      # 枚举分割点
                cost = m[i][k] + m[k+1][j] + p[i] * p[k+1] * p[j+1]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k        # 记录最优分割点
    
    return m, s


def print_optimal_parens(s, i, j):
    """递归打印最优加括号方案（0-indexed）"""
    if i == j:
        print(f"A{i+1}", end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")


# ---- 测试 ----
p = [5, 10, 3, 12, 5]
m, s = matrix_chain_order(p)

n = len(p) - 1
print(f"最少乘法次数: {m[0][n-1]}")
print("最优加括号方案: ", end="")
print_optimal_parens(s, 0, n - 1)
print()

# 打印完整的 m 表
print("\nm 表（最小代价）:")
for i in range(n):
    row = []
    for j in range(n):
        row.append(f"{m[i][j]:6d}" if j >= i else "     -")
    print("  ".join(row))