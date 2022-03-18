class Union_Find():

    def __init__(self):
        self.parent = {}
        self.weight = {}
        self.root = {}

    def build(self, frame):
        if frame not in self.parent:
            self.parent[frame] = frame
            self.weight[frame] = 1
            self.root[frame] = 1

    def findParent(self, frame):
        if self.parent[frame] == frame:
            return frame
        self.parent[frame] = self.findParent(self.parent[frame])
        return self.parent[frame]

    def union(self, frame1, frame2):
        p1 = self.findParent(frame1)
        p2 = self.findParent(frame2)

        if p1 == p2:
            return

        if self.weight[p1] > self.weight[p2]:
            self.parent[p2] = p1
            self.root[p1] += self.root[p2]
            del self.root[p2]
        elif self.weight[p1] < self.weight[p2]:
            self.parent[p1] = p2
            self.root[p2] += self.root[p1]
            del self.root[p1]
        else:
            self.parent[p1] = p2
            self.weight[p2] += 1
            self.root[p2] += self.root[p1]
            del self.root[p1]

