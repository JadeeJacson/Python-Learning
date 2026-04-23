from typing import List
from collections import defaultdict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        pre_sum = 0
        pre_sum_map = defaultdict(int, {0: 1})
        
        for num in nums:
            pre_sum += num
            target = pre_sum - k
            count += pre_sum_map[target]
            pre_sum_map[pre_sum] += 1
            
        return count


# ========== 测试集 ==========

sol = Solution()


# 2. 包含负数
assert sol.subarraySum([-1, -1, 1], 0) == 1         # [-1, 1]
assert sol.subarraySum([1, -1, 0], 0) == 3         # [1,-1], [0], [1,-1,0]

# 3. 单个元素
assert sol.subarraySum([5], 5) == 1
assert sol.subarraySum([5], 3) == 0

# 4. 全0数组（前缀和重复的典型场景）
assert sol.subarraySum([0, 0, 0], 0) == 6           # 所有子数组

# 5. 无匹配
assert sol.subarraySum([1, 2, 3], 7) == 0

# 6. 大k值
assert sol.subarraySum([1, 2, 1, 2, 1], 100) == 0
