class Solution:
    def merge(self, intervals):
        intervals = sorted(intervals)
        index = 0
        while index<len(intervals)-1:
            if(intervals[index][1] >= intervals[index+1][0]):
                if(intervals[index][1] <= intervals[index+1][1]):
                    intervals[index][1] = intervals[index+1][1]                    
                del intervals[index+1]
            else:
                index += 1
        return intervals

inp = [[1,3],[2,6],[8,10],[15,18]]
fcn = Solution()
print(fcn.merge(inp))