import tensorflow as tf
import numpy as np

def predictionCornerPoint(tlf_heatMap, brb_heatMap, threshold):  
    print("Predict Corner Point...")  

    tlf_points = tf.where(tlf_heatMap > threshold[0]).numpy()   
    brb_points = tf.where(brb_heatMap > threshold[1]).numpy()

    print("tlf_points => {}".format([tuple((x, y, z)) for _, x, y, z, _ in tlf_points]))
    print("brb_points => {}".format([tuple((x, y, z)) for _, x, y, z, _ in brb_points]))

    return tlf_points, brb_points


def predictionCornerGroup(tlf_points, brb_points, tlf_group, brb_group):
    print("Predict Corner Group...")  
    
    bboxes = []
    for tlf_point in tlf_points:
        _, x1, y1, z1, _ = tlf_point
        _, x2, y2, z2, _ = min(brb_points, key = lambda pos: abs(brb_group[0][pos[1]][pos[2]][pos[3]][0] - tlf_group[0][x1][y1][z1][0]))
        bboxes.append((x1, y1, z1, x2, y2, z2))

    return bboxes


def predictionBBoxOffset(bboxes, tlf_regression, brb_regression, scale):
    print("Predict Corner Offset...")  

    def offset(x, y, z, regression):
        ox, oy, oz = regression[0][x][y][z]
        return x * scale + ox, y * scale + oy, z * scale + oz
    
    offsetBBoxes = []
    for bbox in bboxes:
        x1, y1, z1, x2, y2, z2 = bbox
        x1, y1, z1 = offset(x1, y1, z1, tlf_regression)
        x2, y2, z2 = offset(x2, y2, z2, brb_regression)
        offsetBBoxes.append((int(x1.numpy()), int(y1.numpy()), int(z1.numpy()), int(x2.numpy()), int(y2.numpy()), int(z2.numpy())))

    return offsetBBoxes


def predictionModel2(predicts, scale, threshold = 0.8):

    tlf_heatMap, tlf_group, tlf_regression = predicts[0: 3]
    brb_heatMap, brb_group, brb_regression = predicts[3: 6]

    tlf_points, brb_points = predictionCornerPoint(tlf_heatMap, brb_heatMap, threshold)
    bboxes                 = predictionCornerGroup(tlf_points, brb_points, tlf_group, brb_group)
    offsetBBoxes           = predictionBBoxOffset(bboxes, tlf_regression, brb_regression, scale)

    return offsetBBoxes