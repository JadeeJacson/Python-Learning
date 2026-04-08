def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    n=len(nums)
    ans=[]
    for i in range(n-2):
        if nums[0]>0:
            break
        if i>0 and nums[i]==nums[i-1]:
            continue
        left,right=i+1,n-1
        while left<right:
            s=nums[left]+nums[right]
            tar=-nums[i]
            if s==0:
                ans.append([nums[i],nums[left],nums[right]])
                while nums[left]==nums[left+1]:
                    left+=1
                while nums[right]==nums[right-1]:
                    right-=1
            if s<0:
                left+=1
            if s>0:
                right-=1
            left+=1
            right-=1
    return ans