from model.create_model import getModel2, getModel3
from data.data_processing import read_image_path, read_groundTruth
import tensorflow as tf
import numpy as np
import os
import time
from skimage import transform

TEST = False

IMAGE_SPATIAL_DIMS = [(128, 128, 128), (128, 128, 128)]
IMAGE_NUM_CHANNELS = [1, 1]
RESIZE_SHAPE = (128, 128, 128)

PATH = "D:\\SANet\\data\\LungNodule\\merge_data"

def get_data(path):
    if not TEST:
        data, target = read_image_path(path, mode = "train"), read_groundTruth(path, mode = "train", resize = RESIZE_SHAPE)
    else:
        num_data = 20
        data = np.random.randn(num_data, 1, IMAGE_SPATIAL_DIMS[0][0], IMAGE_SPATIAL_DIMS[0][1], IMAGE_SPATIAL_DIMS[0][2], 1)
        target = np.random.randint(0, IMAGE_SPATIAL_DIMS[1][0], size = (num_data, 2, 1, 5, 3)) # (_, tlf brb, b, bbox num, dim)        
    return data, target

def create_save_path():
    now = time.localtime(time.time())
    currentTime = "{}_{}{}_{}{}".format(now.tm_year, str(now.tm_mon).zfill(2), str(now.tm_mday).zfill(2), str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2))

    save_path = "./result/{}".format(currentTime)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def predict_model(model):
    image = np.ones((1,) + IMAGE_SPATIAL_DIMS[0] + (IMAGE_NUM_CHANNELS[0],))
    outputs = model(image)
    print("\n======================== predict ========================")
    print("TLF => heatMap    : ", outputs[0].shape)
    print("TLF => group      : ", outputs[1].shape)
    print("TLF => regression : ", outputs[2].shape)
    print("BRB => heatMap    : ", outputs[3].shape)
    print("BRB => group      : ", outputs[4].shape)
    print("BRB => regression : ", outputs[5].shape)

def train():

    if not TEST: save_path = create_save_path()

    # start_epoch = 43
    # model_path = "./result/2022_0804_1703/model_epoch{}".format(str(start_epoch - 1).zfill(3))
    # model = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, model_path)
    # print(model.summary())

    start_epoch = 0
    model = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)
    print(model.summary())

    datas, targets = get_data(PATH)
    num_data = len(datas)

    epochs = 100

    loss_fn   = model.loss
    optimizer = model.optimizer

    for epoch in range(start_epoch, start_epoch + epochs):
        print("\nStart of epoch %d" % (epoch,))

        total_loss = 0
        for step, (data, target) in enumerate(zip(datas, targets)):
            if not TEST:
                path, filename = data, data.split("\\")[-1] + ".npz"
                data = np.load(os.path.join(path, filename))["image"]
                data = data.transpose((0, 2, 3, 1))
                data = transform.resize(data, (1,) + RESIZE_SHAPE)
                data = np.expand_dims(data, -1)
                data = data / np.linalg.norm(data)
                data = data / 255.

            with tf.GradientTape() as tape:
                predicts = model(data, training=True) 
                loss_value = loss_fn(target, predicts)
                total_loss += loss_value

                grads = tape.gradient(loss_value, model.trainable_weights)
                optimizer.apply_gradients(zip(grads, model.trainable_weights))

            print("\r", "Train: %.4f" % (((step + 1) / num_data) * 100.), "%", "(step: {}, loss = {})".format(step, loss_value), end=" ")

        print("save model (total loss = {})".format(total_loss / num_data))
        if not TEST: model.save(os.path.join(save_path, "model_epoch{}".format(str(epoch).zfill(3))))

    predict_model(model)


if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    train()

