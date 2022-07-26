import numpy as np
from .utils.bbox_regression import one_box_transform

TRAIN_THRESHOLD = 0.7

def IOU(bbox1, bbox2):
    pass

def getMaxIOU(bbox, bboxGTs):
    max_ = (0, None)
    for bboxGT in bboxGTs:
        max_ = max(max_, (IOU(bbox, bboxGT), bboxGT))
    return max_

def rpn_loss(regs, clses, targets, anchors):
    bboxGT, clsGT = targets[:, :-1], targets[:, -1]
    
    # classification loss
    N_cls = len(clsGT)
    cls_loss = np.sum(-np.log(clses[:, -1])) / N_cls

    # bounding box loss
    reg_loss = 0
    N_reg = 0
    for anchor, reg in zip(anchors, regs):
        max_iou, max_bbox = getMaxIOU(anchor, bboxGT)
        if max_iou >= TRAIN_THRESHOLD:
            regGT = one_box_transform(anchor, max_bbox)
            reg_loss += np.mean((reg - regGT) ** 2)
            N_reg += 1
    reg_loss /= N_reg

    return reg_loss + cls_loss