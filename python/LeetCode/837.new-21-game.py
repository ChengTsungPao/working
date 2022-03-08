#
# @lc app=leetcode id=837 lang=python3
#
# [837] New 21 Game
#

# @lc code=start
class Solution:
    def new21Game(self, n: int, k: int, maxPts: int) -> float:
        '''
        n = 21, k = 17, maxPts = 10
        score = 12 => 10
                13 => 9 ~ 10
                14 => 8 ~ 10
                15 => 7 ~ 10
                16 => 6 ~ 10 
        '''
        if k == 0:
            return 1.0
        elif n == 0:
            return 0.0

        prob = 1 / maxPts
        dp = [1] * k

        prob_sum = 1
        i, j = 0, 1
        while j < k:
            dp[j] = prob_sum * prob

            prob_sum += dp[j]
            j += 1
            
            if j - i > maxPts:
                prob_sum -= dp[i]
                i += 1

        overProb = 0
        for totalScore in range(max(n - maxPts + 1, 1), k):
            overProb += dp[totalScore] * (maxPts - (n - totalScore)) * prob

        ans = 1 - overProb
        if n < maxPts:
            ans -= (maxPts - n) * prob

        return ans

        
# @lc code=end

