import tensorflow as tf
import numpy as np
import heapq

def predictionCornerPoint(tlf_heatMap, brb_heatMap, numbers):  
    print("Predict Corner Point...")  

    size = tlf_heatMap.shape[1]

    ########################################## heap ##########################################

    tlf_heatMap_heap = [(-tlf_heatMap[0][x][y][z][0], x, y, z) for x in range(size) for y in range(size) for z in range(size)]
    brb_heatMap_heap = [(-brb_heatMap[0][x][y][z][0], x, y, z) for x in range(size) for y in range(size) for z in range(size)]

    heapq.heapify(tlf_heatMap_heap)
    heapq.heapify(brb_heatMap_heap)

    tlf_points = []   
    brb_points = []

    for _ in range(numbers):
        score, x, y, z = heapq.heappop(tlf_heatMap_heap)
        tlf_points.append((-score, x, y, z))

        score, x, y, z = heapq.heappop(brb_heatMap_heap)
        brb_points.append((-score, x, y, z))

    ########################################## sort ##########################################

    # tlf_heatMap_sorted_arr = sorted([(tlf_heatMap[0][x][y][z][0], x, y, z) for x in range(size) for y in range(size) for z in range(size)], key = lambda x: -x[0])
    # brb_heatMap_sorted_arr = sorted([(brb_heatMap[0][x][y][z][0], x, y, z) for x in range(size) for y in range(size) for z in range(size)], key = lambda x: -x[0])

    # tlf_points = []   
    # brb_points = []

    # for i in range(numbers):
    #     score, x, y, z = tlf_heatMap_sorted_arr[i]
    #     tlf_points.append((score, x, y, z))

    #     score, x, y, z = brb_heatMap_sorted_arr[i]
    #     brb_points.append((score, x, y, z))

    ##########################################################################################

    print("tlf_points => {}".format([tuple((x, y, z)) for _, x, y, z in tlf_points]))
    print("brb_points => {}".format([tuple((x, y, z)) for _, x, y, z in brb_points]))

    return tlf_points, brb_points


def predictionCornerGroup(tlf_points, brb_points, tlf_group, brb_group):
    print("Predict Corner Group...")  
    
    bboxes = []
    for score1, x1, y1, z1 in tlf_points:
        for score2, x2, y2, z2 in brb_points:
            L1_distance = abs(tlf_group[0][x1][y1][z1][0] - brb_group[0][x2][y2][z2][0])
            if L1_distance < 0.5:
                bboxes.append(((score1 + score2) / 2, x1, y1, z1, x2, y2, z2))

    return bboxes


def predictionBBoxOffset(bboxes, tlf_regression, brb_regression, scale):
    print("Predict Corner Offset...")  

    def offset(x, y, z, regression):
        ox, oy, oz = regression[0][x][y][z]
        return (x + ox) * scale, (y + oy) * scale, (z + oz) * scale
    
    offsetBBoxes = []
    for bbox in bboxes:
        score, x1, y1, z1, x2, y2, z2 = bbox
        x1, y1, z1 = offset(x1, y1, z1, tlf_regression)
        x2, y2, z2 = offset(x2, y2, z2, brb_regression)
        offsetBBoxes.append((score, int(x1), int(y1), int(z1), int(x2), int(y2), int(z2)))

    return offsetBBoxes


def predictionModel2(predicts, scale, numbers = 100):

    tlf_heatMap, tlf_group, tlf_regression = predicts[0].numpy(), predicts[1].numpy(), predicts[2].numpy()
    brb_heatMap, brb_group, brb_regression = predicts[3].numpy(), predicts[4].numpy(), predicts[5].numpy()

    tlf_points, brb_points = predictionCornerPoint(tlf_heatMap, brb_heatMap, numbers)
    bboxes                 = predictionCornerGroup(tlf_points, brb_points, tlf_group, brb_group)
    offsetBBoxes           = predictionBBoxOffset(bboxes, tlf_regression, brb_regression, scale)

    return offsetBBoxes