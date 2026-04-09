class Solution:
    def trap(self, height: List[int]) -> int:
        left=0
        n=len(height)
        right=n-1
        l_max=r_max=0
        ans=0
        l_max=height[left]
        r_max=height[right]
        while left<right:
            if l_max<=r_max:
                ans+=l_max-height[left]
                left+=1
                l_max=max(l_max,height[left])
            if l_max>r_max:
                ans+=r_max-height[right]
                right-=1
                r_max=max(r_max,height[right])
        return ans