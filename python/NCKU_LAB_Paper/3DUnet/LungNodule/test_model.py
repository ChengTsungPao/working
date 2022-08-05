from model.create_model import getModel2
from model.head.CornerNetHead.utils.prediction import predictionModel2
import tensorflow as tf
import numpy as np
from skimage import transform

IMAGE_SPATIAL_DIMS = [(128, 128, 128), (128, 128, 128)]
IMAGE_NUM_CHANNELS = [1, 1]
RESIZE_SHAPE = (128, 128, 128)


def predict_model(model):
    threshold = (0.4, 0.6)
    
    scale = IMAGE_SPATIAL_DIMS[0][0] // IMAGE_SPATIAL_DIMS[0][1]

    image = np.load("./dataset/0005.npz")["image"]
    image = image.transpose((0, 2, 3, 1))
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
    result = predictionModel2(outputs, scale, threshold)
    print("result => {}".format(result))


def test():
    # model_path = "./result/2022_0802_2335/model_epoch000"
    model_path = "./result/2022_0804_1703/model_epoch010"
    model = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, model_path)
    predict_model(model)

if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

    test()
