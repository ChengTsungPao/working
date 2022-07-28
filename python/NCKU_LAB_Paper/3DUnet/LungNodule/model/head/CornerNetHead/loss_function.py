import tensorflow as tf
import numpy as np
from .utils import prediction as cornerNetPredict


def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5

# heatmaps: predict, points: groundTruth
def loss_det(heatmaps, points, scale, shape):

    alpha, beta = 2, 4
    _, height, width, depth, _ = shape
    
    radius = 2
    def gaussian3D(x, y, z):
        sigma = radius / 3
        return np.e ** -((x * x + y * y + z * z) / (2 * sigma * sigma))

    def penaltyReductionLoss(x, y, z, heapMap):
        one_point_loss = 0
        for i in range(x - radius - 1, x + radius):
            for j in range(y - radius - 1, y + radius):
                for k in range(z - radius - 1, z + radius):
                    if not (0 <= i < height and 0 <= j < width and 0 <= k < depth) or distance([i, j, k], [x, y, z]) > radius:
                        continue
                    
                    p = heapMap[i][j][k][0]
                    if i == x and j == y and k == z:
                        one_point_loss += ((1 - p) ** alpha) * np.log(p)
                    else:
                        # weight
                        y = gaussian3D(abs(i - x), abs(j - y), abs(k - z))
                        one_point_loss += ((1 - y) ** beta) * (p ** alpha) * np.log(1 - p)
        return one_point_loss

    # batch size
    total_loss = batch_size = 0
    for point, heapMap in zip(points, heatmaps):
        # groundTruth point
        current_loss = current_size = 0
        for x, y, z in point:
            x, y, z = x // scale, y // scale, z // scale
            current_loss += penaltyReductionLoss(x, y, z, heapMap)
            current_size += 1

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
            ox, oy, oz = regression[x // scale][y // scale][z // scale][0]
            gx, gy, gz = x / scale - x // scale, y / scale - y // scale, z / scale - z // scale
            mse = (((ox - gx) ** 2 + (oy - gy) ** 2 + (oz - gz) ** 2) / 3) ** 0.5
            current_loss += 0.5 * mse ** 2 if abs(mse) < 1 else abs(mse) - 0.5
            current_size += 1

        total_loss += current_loss / current_size
        batch_size += 1

    return total_loss / batch_size

# points: predict
def loss_pull_push(tlf_points, brb_points):
    # batch size
    total_pull_loss = total_push_loss = batch_size = 0
    for tlf_point, brb_point in zip(tlf_points, brb_points):
        # predict point

        # pull loss
        center = []
        current_loss = current_size = 0
        for x1, y1, z1 in tlf_point:
            x2, y2, z2 = min(brb_point, key = lambda element: distance(element, [x1, y1, z1]))
            x, y, z = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
            center.append((x, y, z))
            current_loss += distance([x1, y1, z1], [x, y, z]) ** 2 + distance([x2, y2, z2], [x, y, z]) ** 2
            current_size += 1
        total_pull_loss += current_loss / current_size

        # push loss
        current_loss = current_size = 0
        for i, (x, y, z) in enumerate(center):
            for j, (x_, y_, z_) in enumerate(center):
                if i != j:
                    current_loss += max(0, distance([x, y, z], [x_, y_, z_]))
        total_push_loss += current_loss / current_size

        batch_size += 1

    return total_pull_loss / batch_size, total_push_loss / batch_size

def cornerNetLoss(predicts, targets, scale, parameter):
    alpha, beta, gamma = parameter
    
    tlf_predict, brb_predict = predicts

    tlf_heatMap_predict, tlf_group_predict, tlf_regression_predict = tlf_predict
    brb_heatMap_predict, brb_group_predict, brb_regression_predict = brb_predict

    # tlf_point_predict, brb_point_predict = cornerNetPredict.modelPrediction2(tlf_predict, brb_predict)
    tlf_point_target , brb_point_target  = targets
    
    heatMap_shape = tlf_heatMap_predict.shape
    tlf_loss_det , brb_loss_det  = loss_det(tlf_heatMap_predict, tlf_point_target, scale, heatMap_shape), loss_det(brb_heatMap_predict, brb_point_target, scale, heatMap_shape)
    tlf_loss_off , brb_loss_off  = loss_off(tlf_regression_predict, tlf_point_target, scale), loss_off(brb_regression_predict, brb_point_target, scale)
    loss_pull    , loss_push     = loss_pull_push(tlf_group_predict, brb_group_predict)

    # tlf_loss_det , brb_loss_det  = 0, 0
    # tlf_loss_off , brb_loss_off  = 0, 0
    # loss_pull    , loss_push     = 0, 0

    return (tlf_loss_det + brb_loss_det) + alpha * loss_pull + beta * loss_push + gamma * (tlf_loss_off + brb_loss_off)