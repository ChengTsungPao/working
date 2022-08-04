import tensorflow as tf
import numpy as np
from .utils import prediction as cornerNetPredict

# heatmaps: predict, points: groundTruth
def loss_det(heatmaps, points, scale, shape):

    alpha, beta = 2, 4
    _, height, width, depth, _ = shape
    
    radius = 2
    def gaussian3D(x, y, z):
        sigma = radius / 3
        return np.e ** -((x * x + y * y + z * z) / (2 * sigma * sigma))

    def distance(point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5

    def getHeapMapWeight(x, y, z, heapMapWeight):
        for i in range(x - radius - 1, x + radius):
            for j in range(y - radius - 1, y + radius):
                for k in range(z - radius - 1, z + radius):
                    if 0 <= i < height and 0 <= j < width and 0 <= k < depth and distance([i, j, k], [x, y, z]) <= radius:
                        heapMapWeight[i][j][k][0] = max(heapMapWeight[i][j][k][0], gaussian3D(abs(i - x), abs(j - y), abs(k - z)))

    def backgroundLoss(heapMap, heapMapWeight):
        y = heapMapWeight
        p = heapMap
        return tf.math.reduce_sum(((1 - y) ** beta) * (p ** alpha) * np.log(1 - p + 10 ** -7))

    # batch size
    total_loss = batch_size = 0
    for point, heapMap in zip(points, heatmaps):
        # groundTruth point
        current_loss = current_size = 0
        heapMap = tf.clip_by_value(heapMap, 0, 1)
        heapMapWeight = np.zeros(heapMap.shape, float)
        for x, y, z in point:
            x, y, z = x // scale, y // scale, z // scale
            getHeapMapWeight(x, y, z, heapMapWeight)

            p = heapMap[x][y][z][0]
            current_loss += ((1 - p) ** alpha) * np.log(p + 10 ** -7)
            current_size += 1

        current_loss += backgroundLoss(heapMap, heapMapWeight)

        total_loss += -current_loss / current_size
        batch_size += 1

    return total_loss / batch_size

# regressions: predict, points: groundTruth
def loss_off(regressions, points, scale):
    # batch size
    total_loss = batch_size = 0
    for point, regression in zip(points, regressions):
        # groundTruth point
        current_loss = current_size = 0
        for x, y, z in point:
            ox, oy, oz = regression[x // scale][y // scale][z // scale]
            gx, gy, gz = x / scale - x // scale, y / scale - y // scale, z / scale - z // scale
            mse = (abs(ox - gx) + abs(oy - gy) + abs(oz - gz)) / 3
            current_loss += 0.5 * mse ** 2 if abs(mse) < 1 else abs(mse) - 0.5
            current_size += 1

        total_loss += current_loss / current_size
        batch_size += 1

    return total_loss / batch_size

def loss_pull_push(tlf_groups, brb_groups, tlf_points, brb_points, scale):
    # batch size

    total_pull_loss = total_push_loss = batch_size = 0
    for tlf_group, brb_group, tlf_point, brb_point in zip(tlf_groups, brb_groups, tlf_points, brb_points):

        # pull loss
        center = []
        current_loss = current_size = 0
        for (x1, y1, z1), (x2, y2, z2) in zip(tlf_point, brb_point):
            x1, y1, z1 = x1 // scale, y1 // scale, z1 // scale
            x2, y2, z2 = x2 // scale, y2 // scale, z2 // scale            
            etk, ebk = tlf_group[x1][y1][z1][0], brb_group[x2][y2][z2][0]
            ek = (etk + ebk) / 2
            center.append(ek)
            current_loss += (etk - ek) ** 2 + (ebk - ek) ** 2
            current_size += 1
        total_pull_loss += current_loss / current_size

        # push loss
        delta = 1
        current_loss = current_size = 0
        for i, ei in enumerate(center):
            for j, ej in enumerate(center):
                if i != j:
                    current_loss += max(0, delta - abs(ei - ej))
                    current_size += 1
        total_push_loss += current_loss / ((current_size) * (current_size - 1)) if current_size > 1 else current_loss

        batch_size += 1

    return total_pull_loss / batch_size, total_push_loss / batch_size

def cornerNetLoss(predicts, targets, scale):
    alpha, beta, gamma = 0.1, 0.1, 1

    tlf_heatMap_predict, tlf_group_predict, tlf_regression_predict = predicts[0: 3]
    brb_heatMap_predict, brb_group_predict, brb_regression_predict = predicts[3: 6]

    # tlf_point_predict, brb_point_predict = cornerNetPredict.modelPrediction2(tlf_predict, brb_predict)
    tlf_point_target , brb_point_target  = targets
    
    heatMap_shape = tlf_heatMap_predict.shape
    tlf_loss_det , brb_loss_det  = loss_det(tlf_heatMap_predict, tlf_point_target, scale, heatMap_shape), loss_det(brb_heatMap_predict, brb_point_target, scale, heatMap_shape)
    tlf_loss_off , brb_loss_off  = loss_off(tlf_regression_predict, tlf_point_target, scale), loss_off(brb_regression_predict, brb_point_target, scale)
    loss_pull    , loss_push     = loss_pull_push(tlf_group_predict, brb_group_predict, tlf_point_target, brb_point_target, scale)

    # tlf_loss_det , brb_loss_det  = 0, 0
    # tlf_loss_off , brb_loss_off  = 0, 0
    # loss_pull    , loss_push     = 0, 0

    return (tlf_loss_det + brb_loss_det) + alpha * loss_pull + beta * loss_push + gamma * (tlf_loss_off + brb_loss_off)