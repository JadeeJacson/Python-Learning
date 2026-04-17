def knapsack_2d_with_trace(capacity, weights, values):
    n = len(weights)
    # 创建二维数组 dp，行数为 n+1，列数为 capacity+1，初始全为 0
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # --- 1. 填表过程（与你的代码一致） ---
    for i in range(1, n + 1):
        current_weight = weights[i-1]
        current_value = values[i-1]

        for j in range(1, capacity + 1):
            if current_weight > j:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j - current_weight] + current_value)
                
    # --- 2. 新增：追踪最优解过程 ---
    selected_items = [] # 用于记录被选中的物品编号（从 1 开始计数）
    j = capacity        # 从最大容量开始往回找
    
    # 从右下角，也就是最后一件物品开始倒推
    for i in range(n, 0, -1):
        if j == 0:
            break # 如果背包没容量了，直接提前结束
            
        # 如果当前格子的值不等于正上方的格子，说明这件物品被装入了
        if dp[i][j] != dp[i-1][j]:
            selected_items.append(i)          # 记录这是第 i 件物品
            j -= weights[i-1]                 # 减去这件物品的重量，得到剩余容量
            
    # 因为是从后往前倒推的，所以列表是倒序的。反转一下让输出更直观（可选）
    selected_items.reverse()
    
    return dp[n][capacity], selected_items

# --- 测试 ---
capacity = 4
weights = [1, 3, 4]
values = [15, 20, 30]

max_val, items = knapsack_2d_with_trace(capacity, weights, values)
print(f"最大价值是: {max_val}")
print(f"选中的物品是 (第几个): {items}") 

# 验证一下：
# 第 1 件 (重量1, 价值15) + 第 2 件 (重量3, 价值20) = 总重量4, 总价值35


def knapsack_1d(capacity, weights, values):
    n = len(weights)
    # 只需要一个一维数组，代表各个容量下的最大价值
    dp = [0] * (capacity + 1)
    
    # 遍历每件物品
    for i in range(n):
        current_weight = weights[i]
        current_value = values[i]
        
        # 遍历背包容量，注意：必须倒序遍历！
        # 且只需要遍历到 j >= current_weight 即可，装不下的不管它，继承旧值
        for j in range(capacity, current_weight - 1, -1):
            
            # 状态转移：保持原状(不拿) vs 腾出空间拿当前物品
            dp[j] = max(dp[j], dp[j - current_weight] + current_value)
            
    return dp[capacity]

# 测试
print("优化后最大价值是:", knapsack_1d(capacity, weights, values)) # 输出 35