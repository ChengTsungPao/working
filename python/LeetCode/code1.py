class Binary_Indexed_Tree():
    def __init__(self, n):
        self.tree = [0] * (n + 1)
        
    def lowbit(self, x):
        return x & -x
    
    def update(self, index, delta):
        while index < len(self.tree):
            self.tree[index] += delta
            index += self.lowbit(index)
            
    def quary(self, index):
        ans = 0
        while index > 0:
            ans += self.tree[index]
            index -= self.lowbit(index)
        return ans


def countSmaller(nums):

    # time complexity: O(nlogn)
    # space complexity: O(n)
    
    # 概念: 將Binary_Indexed_Tree的delta都設為1，來統計數量
    # 方法: 由右而左update，在quary的時候只會有該index右邊的數字參與，且只有較小的數字(rank)會被加起來 (因為有sort)
    # 注意: 但須注意不能quary與自己大小相同的數字 (rank[nums[i]] - 1)
    
    # 比起另一個方法多了一個sort，速度會較慢，但較省空間，且能處理有小數點的情況
    
    rank = {}
    sorted_nums = sorted(set(nums))
    for i in range(len(sorted_nums)):
        rank[sorted_nums[i]] = i + 1
    
    BIT = Binary_Indexed_Tree(len(sorted_nums))
    
    ans = []
    for i in range(len(nums)):
        ans.append(BIT.quary(rank[nums[i]]))
        BIT.update(rank[nums[i]], 1)
        
    return ans[::-1]


def function(data):

    for i in range(len(data)):
        data[i].append(i)

    nums = []
    data.sort()
    for i in range(len(data)):
        x, y, index = data[i]
        nums.append(y)

    count = countSmaller(nums)
    count.reverse()

    ans = [0] * len(data)
    for i in range(len(data)): 
        x, y, index = data[i]
        ans[index] = count[i]

    return ans


data = [
    [3, 1],
    [4, 1],
    [5, 9],
    [2, 6],
    [5, 3],
    [5, 8],
    [9, 7]
]

data = [
    [1, 2],
    [3, 4],
    [5, 6],
    [7, 8],
    [9, 10]
]

data = [
    [961, 404],
    [640, 145],
    [983, 888],
    [539, 71],
    [437, 532]
]

print(function(data))








