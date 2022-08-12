import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.create_model import getModel3
from data.segm_data_processing import getInferenceGenerator
import tensorflow as tf
import numpy as np
import cv2
import collections
import matplotlib.pylab as plt


TEST = True

THRESHOLD = 0.5

IMAGE_SPATIAL_DIMS = (512, 512, 32)
IMAGE_NUM_CHANNELS = 1
SAVE_PATH = "./result/2022_0812_1253_3dunet/"
DATA_PATH = "E:\\dataset\\NCKU\\Lung\\train\\"


def predict_model(model_path):

    def transfer(image):
        image = np.squeeze(image, axis =  0)
        image = np.squeeze(image, axis = -1)
        image = image.transpose((2, 0, 1))
        return image

    model = getModel3(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, model_path)

    for datas, sliceIDList, patientID in getInferenceGenerator(DATA_PATH):
        outputs = model(datas)

        startSliceID, endSliceID = str(sliceIDList[0]).zfill(3), str(sliceIDList[-1]).zfill(3)

        print("====================== patientID = {}, sliceID = {} ~ {} (max score = {}) ======================".format(patientID, startSliceID, endSliceID, np.max(outputs)))

        heapMaps   = transfer(outputs)
        
        binaryMaps = np.where(outputs > THRESHOLD, 255, 0)
        binaryMaps = np.array(binaryMaps, int)
        binaryMaps = transfer(binaryMaps)

        count = collections.Counter(binaryMaps.flatten())
        print("status = {}".format(str(count)))
        
        save_path = os.path.join(model_path.split(".hdf5")[0], "patientID={},sliceID={}~{}".format(patientID, startSliceID, endSliceID))

        for heapMap, binaryMap, sliceID in zip(heapMaps, binaryMaps, sliceIDList):
            heapMap_name = "heapMap,patientID={},sliceID={}.jpg".format(patientID, str(sliceID).zfill(3))
            binaryMap_name = "binaryMap,patientID={},sliceID={}.jpg".format(patientID, str(sliceID).zfill(3))
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            plt.clf()
            plt.imshow(heapMap, cmap = "hot")
            plt.colorbar()
            plt.savefig(os.path.join(save_path, heapMap_name))

            cv2.imwrite(os.path.join(save_path, binaryMap_name), binaryMap)

def test():
    model_path = os.path.join(SAVE_PATH, "model-15.hdf5")
    predict_model(model_path)


if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    test()

