import numpy as np


def evaluation(predict, groundTruth): # pos = [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
    if len(predict) == 0:
        return 0, 0, 0, 0

    predictPos = boundingBoxAreaPos(predict)
    groundTruthPos = boundingBoxAreaPos(groundTruth)

    IOU = len(predictPos & groundTruthPos) / len(predictPos | groundTruthPos)
    recall = len(predictPos & groundTruthPos) / len(groundTruthPos)
    precision = len(predictPos & groundTruthPos) / len(predictPos)

    if recall == 0 and precision == 0:
        f1_score = 0
    else:
        f1_score = 2 / (recall ** -1 + precision ** -1)

    return IOU, recall, precision, f1_score


def boundingBoxAreaPos(position):
    position = np.array(position)
    pos1, pos2, pos3, pos4 = position

    def line1(pos):
        a, b = np.array(pos1) - np.array(pos2)
        return a * pos[0] + b * pos[1]

    def line2(pos):
        a, b = np.array(pos2) - np.array(pos3)
        return a * pos[0] + b * pos[1]

    line1_range = sorted([line1(pos1), line1(pos2)])
    line2_range = sorted([line2(pos2), line2(pos3)])

    found = set()
    minX = np.min(position[:, 0])
    minY = np.min(position[:, 1])
    maxX = np.max(position[:, 0])
    maxY = np.max(position[:, 1])
    for i in range(minX, maxX + 1):
        for j in range(minY, maxY + 1):
            pos = (i, j)
            if line1_range[0] <= line1(pos) <= line1_range[1] and line2_range[0] <= line2(pos) <= line2_range[1]:
                found.add(pos)

    return found
