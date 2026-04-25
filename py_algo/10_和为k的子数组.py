from typing import List
from collections import defaultdict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        cnt=0
        ps=0
        ps_map=defaultdict(int,{0:1})

        for num in nums:
            ps+=num
            tar=ps-k
            cnt+=ps_map[tar]   #这里会创tar的键值对，但不会加一，没影响
            ps_map[ps]+=1      #值的累计考虑到了末尾元素相同，但不同长度的数组
        return cnt


# ========== 测试集 ==========

sol = Solution()
assert sol.subarraySum([-1, -1, 1,2,1,1,1,-2,-3,1], 1) == 1         # [-1, 1]


'''
把前缀和想象成海拔高度，你在爬山：
k=7时
高度:  0    3    7   14   16   13   14   18   20
       |    |    |    |    |    |    |    |    |
位置:  0    1    2    3    4    5    6    7    8
       ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑    ↑
      起点  3    4    7    2   -3    1    4    2

你在每个位置问："我之前有没有站在过比现在低 7 米的地方？"
'''