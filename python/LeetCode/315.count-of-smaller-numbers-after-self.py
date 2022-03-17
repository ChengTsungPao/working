#
# @lc app=leetcode id=315 lang=python3
#
# [315] Count of Smaller Numbers After Self
#

# @lc code=start
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        
        n = len(nums)

        ans = [0] * n
        nums = [(nums[index], index) for index in range(n)]

        def mergeSort(left, right):
            if left == right:
                return [(nums[left], 0)]

            mid = left + (right - left) // 2
            leftArr = mergeSort(left, mid)
            rightArr = mergeSort(mid + 1, right)

            arr = []
            i = j = 0
            while i < len(leftArr) and j < len(rightArr):
                leftNum, leftIndex = leftArr[i]
                rightNum, rightIndex = rightArr[j]
                if leftNum > rightNum:
                    ans[leftIndex] += 1
                    arr.append((rightNum, rightIndex))
                    j += 1
                else:
                    arr.append((leftNum, leftIndex))
                    i += 1

            if i < len(leftArr):
                arr += leftArr

            if j < len(rightArr):
                arr += rightArr

            return arr

        mergeSort(0, n - 1)
        return ans

# @lc code=end

