#
# @lc app=leetcode id=975 lang=python3
#
# [975] Odd Even Jump
#

# @lc code=start
import collections

class Node:
    def __init__(self, index = 0, val = 0):
        self.index = index
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, index, val):
        def _insert(root, index, val):
            if not root:
                return Node(index, val)
            if val <= root.val:
                root.left = _insert(root.left, index, val)
            else:
                root.right = _insert(root.right, index, val)
            return root
        self.root = _insert(self.root, index, val)

    def searchMaxClose(self, val):
        def _searchMaxClose(root, val):
            if not root:
                return float("inf"), float("inf")
            if val <= root.val:
                return min((root.val - val, root.index), _searchMaxClose(root.left, val))
            else:
                return _searchMaxClose(root.right, val)
        return _searchMaxClose(self.root, val)[1]

    def searchMinClose(self, val):
        def _searchMinClose(root, val):
            if not root:
                return float("inf"), float("inf")
            if val < root.val:
                return _searchMinClose(root.left, val)
            if val == root.val:
                return min((val - root.val, root.index), _searchMinClose(root.left, val))
            else:
                return min((val - root.val, root.index), _searchMinClose(root.right, val))
        return _searchMinClose(self.root, val)[1]
        
    def remove(self, index, val):
        def _remove(root, index, val):
            if not root:
                return None
            if val < root.val:
                root.left = _remove(root.left, index, val)
            elif val > root.val:
                root.right = _remove(root.right, index, val)
            else:
                if not root.left:
                    node = root.right
                    root.right = None
                    return node
                elif not root.right:
                    node = root.left
                    root.left = None
                    return node
                predecessor = root.left
                while predecessor.right:
                    predecessor = predecessor.right
                root.val = predecessor.val
                root.index = predecessor.index
                predecessor.val = val
                predecessor.index = index
                root.left = _remove(root.left, index, val)
            return root
        self.root = _remove(self.root, index, val)


class Solution:
    def oddEvenJumps(self, arr):

        n = len(arr)
        
        tree = BST()
        for index in range(n):
            tree.insert(index, arr[index])

        graph = collections.defaultdict(list)
        tree.remove(0, arr[0])
        evenIndex = tree.searchMaxClose(arr[0])
        graph[evenIndex, False].append(0)

        for index in range(1, n):
            tree.remove(index, arr[index])
            evenIndex = tree.searchMaxClose(arr[index])
            oddIndex = tree.searchMinClose(arr[index])

            graph[evenIndex, False].append(index)
            graph[oddIndex, True].append(index)

        
        def recur(index, isOdd):
            ret = set([index]) if isOdd else set()
            if len(graph[index, isOdd]) == 0:
                return ret
            for nextIndex in graph[index, isOdd]:
                ret |= recur(nextIndex, not isOdd)
            return ret

        return len(recur(n - 1, True) | recur(n - 1, False))

        
# @lc code=end

