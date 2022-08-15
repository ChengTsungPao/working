import os
from pyexpat import model
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.create_model import getModel4
from data.segm_data_processing import getGernerator
import tensorflow as tf
import numpy as np
import os
import time

IMAGE_SPATIAL_DIMS = (512, 512, 32)
IMAGE_NUM_CHANNELS = 1

PATH = "D:\\SANet\\data\\LungNodule\\merge_data"

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
    save_path = create_save_path()

    train_path, target_path = "D:\\SANet\\data\\LungNodule\\merge_data\\train", "E:\\04_NewLn_Database\\label"
    test_path , target_path = "D:\\SANet\\data\\LungNodule\\merge_data\\test" , "E:\\04_NewLn_Database\\label"

    trainGernerator = getGernerator(train_path, target_path)
    testGernerator  = getGernerator(test_path, target_path)

    start_epoch = 0
    model_path = None #".\\result\\2022_0811_2240_3dunet\\model-{}.hdf5".format(str(start_epoch).zfill(2))
    model = getModel4(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, model_path)
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(os.path.join(save_path, "model-{epoch:02d}.hdf5"), monitor = 'loss', verbose = 1)
    model.fit_generator(trainGernerator, steps_per_epoch = 2280, epochs = 100, callbacks = [model_checkpoint], initial_epoch = start_epoch) # 2280
    # predict_model(model)

if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    train()