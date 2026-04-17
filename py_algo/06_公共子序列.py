def lcs(X, Y):
    m, n = len(X), len(Y)
    # 建立 dp 表，大小 (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:           # 字符相等：对角线 +1
                dp[i][j] = dp[i-1][j-1] + 1
            else:                            # 字符不等：取上/左最大值
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n], dp

def backtrack(dp, X, Y):
    """回溯找出具体的 LCS 字符串"""
    i, j = len(X), len(Y)
    lcs_str = []
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs_str.append(X[i-1])
            i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(lcs_str))

X = "ABCBDAB"
Y = "BDCAB"
length, dp = lcs(X, Y)
result = backtrack(dp, X, Y)
print(f"LCS 长度: {length}")   # 4
print(f"LCS 字符串: {result}") # BCAB
