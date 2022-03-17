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
        count = 0
        total_dection = len(predict)
        total_groundTruth = len(groundTruth.root)

        for i in range(total_dection):
            find = False
            for f in range(predict[i] - delta, predict[i] + delta + 1):
                if f in groundTruth.parent:
                    frame = groundTruth.findParent(f)
                    groundTruth.root[frame] = True
                    find = True
            if find == False:
                count += 1
                
        precision = (total_dection - count) / total_dection
        recall = sum(groundTruth.root.values()) / total_groundTruth
        FSR = count / total

        return precision, recall, FSR