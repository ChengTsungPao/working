import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.create_model import getModel2
from model.head.CornerNetHead.utils.prediction import predictionModel2
import tensorflow as tf
import numpy as np
from skimage import transform

IMAGE_SPATIAL_DIMS = [(128, 128, 128), (128, 128, 128)]
IMAGE_NUM_CHANNELS = [1, 1]
RESIZE_SHAPE = (128, 128, 128)


def predict_model(model):

    def overlapping(bbox1, bbox2):
        x1, x2 = max(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1])
        y1, y2 = max(bbox1[2], bbox2[2]), min(bbox1[3], bbox2[3])
        z1, z2 = max(bbox1[4], bbox2[4]), min(bbox1[5], bbox2[5])
        return max(x2 - x1 + 1, 0) * max(y2 - y1 + 1, 0) * max(z2 - z1 + 1, 0)

    def getArea(bbox):
        return (bbox[1] - bbox[0] + 1) * (bbox[3] - bbox[2] + 1) * (bbox[5] - bbox[4] + 1)
    
    scale = IMAGE_SPATIAL_DIMS[0][0] // IMAGE_SPATIAL_DIMS[0][1]
    numbers = 1000

    image = np.load("./dataset/0084.npz")["image"]
    image = image.transpose((0, 2, 3, 1))
    IMAGE_SHAPE = image.shape

    image = transform.resize(image, (1,) + RESIZE_SHAPE)
    image = np.expand_dims(image, -1)
    image = image / 255.

    outputs = model(image)
    print("\n======================== predict ========================")
    print("TLF => heatMap    : {} (max: {:.7f}, min: {:.7f})".format(outputs[0].shape, np.max(outputs[0]), np.min(outputs[0])))
    print("TLF => group      : {}".format(outputs[1].shape))
    print("TLF => regression : {}".format(outputs[2].shape))
    print("BRB => heatMap    : {} (max: {:.7f}, min: {:.7f})".format(outputs[3].shape, np.max(outputs[3]), np.min(outputs[3])))
    print("BRB => group      : {}".format(outputs[4].shape))
    print("BRB => regression : {}".format(outputs[5].shape))

    print("\n======================== result ========================")
    result = predictionModel2(outputs, scale, numbers)
    area, bbox = 0, (-1, -1, -1, -1, -1, -1)
    # gx1, gx2, gy1, gy2, gz1, gz2 = 400, 425, 236, 261, 160, 172
    # gx1, gx2, gy1, gy2, gz1, gz2 = 314, 359, 309, 341, 228, 259
    # gx1, gx2, gy1, gy2, gz1, gz2 = 325, 354, 280, 300, 58, 70
    gx1, gx2, gy1, gy2, gz1, gz2 = 94, 152, 229, 312, 244, 309

    for score, x1, y1, z1, x2, y2, z2 in result:
        # z1, z2 = 0, 0
        # gz1, gz2 = 0, 0
        bbox1 = (x1 * 4, x2 * 4, y1 * 4, y2 * 4, z1 * IMAGE_SHAPE[-1] // 128, z2 * IMAGE_SHAPE[-1] // 128)
        bbox2 = (gx1, gx2, gy1, gy2, gz1, gz2)
        try:
            area, bbox = max((area, bbox), (overlapping(bbox1, bbox2) / (getArea(bbox1) + getArea(bbox2) - overlapping(bbox1, bbox2)), bbox1))
        except:
            pass

    # print("result => {}".format(result))
    print("result => {}".format(bbox))


def test():
    # model_path = "./result/2022_0802_2335/model_epoch000"
    model_path = "./result/2022_0804_1703/model_epoch042"
    model = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, model_path)
    predict_model(model)

if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

    test()
