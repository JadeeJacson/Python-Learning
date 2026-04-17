def maxSubArrayAndIndices(nums):
    current_sum = nums[0]
    max_sum = nums[0]
    
    temp_start = 0  # 临时起点
    start = 0       # 最终最大子数组的起点
    end = 0         # 最终最大子数组的终点
    
    for i in range(1, len(nums)):
        # 如果另起炉灶比较好
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            temp_start = i # 临时起点变为当前位置
        else:
            current_sum = current_sum + nums[i]
            
        # 如果找到了更大的总和
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start # 确认真正的起点
            end = i            # 确认真正的终点
            
    return max_sum, nums[start:end+1] # 切片右边界是开区间，所以要 end+1

nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_val, sub_arr = maxSubArrayAndIndices(nums)
print(f"最大和: {max_val}, 子数组: {sub_arr}")
# 输出: 最大和: 6, 子数组: [4, -1, 2, 1]
