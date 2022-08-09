import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.create_model import getModel3
from data.data_processing import read_image_path, read_groundTruth
import tensorflow as tf
import numpy as np
import os
import time
from skimage import transform

TEST = True

IMAGE_SPATIAL_DIMS = (512, 512, 128)
IMAGE_NUM_CHANNELS = 1

PATH = "D:\\SANet\\data\\LungNodule\\merge_data"

def get_data(path):
    if not TEST:
        data, target = read_image_path(path, mode = "train"), read_groundTruth(path, mode = "train")
    else:
        num_data = 20
        data = np.random.randn(num_data, 1, IMAGE_SPATIAL_DIMS[0][0], IMAGE_SPATIAL_DIMS[0][1], IMAGE_SPATIAL_DIMS[0][2], 1)
        target = np.random.randint(0, IMAGE_SPATIAL_DIMS[1][0], size = (num_data, 2, 1, 5, 3)) # (_, tlf brb, b, bbox num, dim)        
    return data, target

def create_save_path():
    now = time.localtime(time.time())
    currentTime = "{}_{}{}_{}{}_3dunet".format(now.tm_year, str(now.tm_mon).zfill(2), str(now.tm_mday).zfill(2), str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2))

    save_path = "./result/{}".format(currentTime)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def predict_model(model):
    image = np.ones((1,) + IMAGE_SPATIAL_DIMS + (IMAGE_NUM_CHANNELS,))
    outputs = model(image)
    print("\n======================== predict ========================")
    print("shape => ", outputs.shape)

def train():
    model = getModel3(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)
    predict_model(model)


if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    train()

