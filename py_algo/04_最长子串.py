class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char=set()
        left=0
        ans=0
        for right in range(len(s)):
            while s[right] in char:
                char.remove(s[left])
                left+=1
            char.add(s[right])
            ans=max(ans,len(char))
        return ans
    

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char={}
        left=0
        ans=0
        for right,ch in enumerate(s):
            if ch in char and char[ch]>=left:
                left=char[ch]+1
            char[ch]=right
            ans=max(ans,len(char))
        return ans