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


    def getAccuracy(self, predict, groundTruth, total, delta = 0):
        TP = FP = 0
        total_groundTruth = len(groundTruth.parent)

        for i in range(len(predict)):
            find = False
            for f in range(predict[i] - delta, predict[i] + delta + 1):
                if f in groundTruth.parent:
                    frame = groundTruth.findParent(f)
                    TP += groundTruth.root[frame]
                    groundTruth.root[frame] = 0
                    find = True
            if find == False:
                FP += 1

        total_dection = TP + FP

        precision = TP / total_dection
        recall = TP / total_groundTruth
        FPR = FP / (total - total_groundTruth)

        return precision, recall, FPR