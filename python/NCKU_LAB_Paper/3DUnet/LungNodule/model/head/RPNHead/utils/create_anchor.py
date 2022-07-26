import numpy as np
import itertools

BASES = [5, 10, 20, 30, 50]
RATIOS = [[1, 1, 1]]

def get_anchors(bases = BASES, aspect_ratios = RATIOS):
    anchors = []
    for b in bases:
        for asp in aspect_ratios:
            d, h, w = b * asp[0], b * asp[1], b * asp[2]
            anchors.append([d, h, w])

    return anchors

def make_rpn_windows(image_shape, stride = [1, 1, 1]):
    strideZ, strideY, strideX = stride
    offsetZ, offsetY, offsetX = (float(strideZ) - 1) / 2, (float(strideY) - 1) / 2, (float(strideX) - 1) / 2
    anchors = get_anchors()
    D, H, W = image_shape
    oz = np.arange(offsetZ, offsetZ + strideZ * (D - 1) + 1, strideZ)
    oh = np.arange(offsetY, offsetY + strideY * (H - 1) + 1, strideY)
    ow = np.arange(offsetX, offsetX + strideX * (W - 1) + 1, strideX)

    windows = []
    for z, y, x, a in itertools.product(oz, oh, ow, anchors):
        windows.append([z, y, x, a[0], a[1], a[2]])
    windows = np.array(windows)

    return windows