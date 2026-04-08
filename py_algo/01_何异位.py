import collections

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        a = collections.defaultdict(list)
        for word in strs:
            sorted_word = "".join(sorted(word))
            a[sorted_word].append(word)
        return list(a.values())

print(Solution().groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))


