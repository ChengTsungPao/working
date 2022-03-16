class data_analyze():

    def __init__(self):
        pass


    def dataAdjust(self, result):
        result.append(float("inf"))
        ans = []
        for i in range(len(result) - 1):
            if result[i] + 1 != result[i + 1]:
                ans.append(result[i])
        return ans


    def getAccuracy(self, result, groundTruth, delta = 0):
        count = 0
        total_dection = len(result)
        total_groundTruth = len(groundTruth.root)

        for i in range(total_dection):
            find = False
            for f in range(result[i] - delta, result[i] + delta + 1):
                if f in groundTruth.parent:
                    frame = groundTruth.findParent(f)
                    groundTruth.root[frame] = True
                    find = True
            if find == False:
                count += 1
                
        precision = (total_dection - count) / total_dection
        recall = sum(groundTruth.root.values()) / total_groundTruth

        return precision, recall
