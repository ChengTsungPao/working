#
# @lc app=leetcode id=313 lang=python3
#
# [313] Super Ugly Number
#

# @lc code=start
class Solution:
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:

        uglyNums = [1]
        index_of_prime = [0] * len(primes)

        heap = []
        for i in range(len(primes)):
            candidateNum = uglyNums[index_of_prime[i]] * primes[i]
            heap.append((candidateNum, i))

        i = 0
        while i < n - 1:
            number, index = heapq.heappop(heap)

            if number <= uglyNums[-1]:
                continue

            uglyNums.append(number)
            index_of_prime[index] += 1

            candidateNum = uglyNums[index_of_prime[index]] * primes[index]
            heapq.heappush(heap, (candidateNum, index))

            i += 1

        return uglyNums[-1]

# @lc code=end

