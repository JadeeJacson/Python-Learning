def activity_selection(activities):
    """
    贪心算法：活动安排问题
    activities: list of (start, end)
    返回：选中的活动列表
    """
    # Step 1: 按结束时间升序排序
    sorted_acts = sorted(activities, key=lambda x: x[1])
    
    selected = [sorted_acts[0]]   # 先选第一个（结束最早）
    last_end = sorted_acts[0][1]  # 记录上一个选中活动的结束时间
    
    # Step 2: 遍历剩余活动
    for act in sorted_acts[1:]:
        start, end = act
        if start >= last_end:   # 不重叠（开始时间 >= 上一个结束时间）
            selected.append(act)
            last_end = end
    
    return selected

# 测试
activities = [(1,4), (3,5), (0,6), (5,7), (8,9), (5,9)]
result = activity_selection(activities)
print("选中活动:", result)
print("数量:", len(result))


def greedy_loading(weights, C):
    """
    最优装载贪心算法
    返回：选中的原始下标列表、装载数量、总重量
    """
    # 记录原始下标，排序
    indexed = sorted(enumerate(weights), key=lambda x: x[1])
    
    selected = []
    total = 0
    
    for orig_idx, w in indexed:
        if total + w <= C:
            selected.append(orig_idx)
            total += w
        else:
            break  # 后面更重，也装不下（已排序）
    
    return selected, len(selected), total

weights = [10, 5, 20, 8, 15, 3]
C = 30
sel, count, total_w = greedy_loading(weights, C)

print(f"排序后重量: {sorted(weights)}")
print(f"选中箱子（原编号）: {[i+1 for i in sel]}")
print(f"装载数量: {count}，总重量: {total_w}")