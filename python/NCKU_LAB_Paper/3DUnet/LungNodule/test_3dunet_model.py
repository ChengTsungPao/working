from operator import mod
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
from glob import glob

TEST = True

MODE = "test"
THRESHOLD = 0.6

IMAGE_SPATIAL_DIMS = (512, 512, 32)
IMAGE_NUM_CHANNELS = 1

MODEL_NAME = "model-70.hdf5"
SAVE_PATH = "./result/2022_0812_1253_3dunet/"
DATA_PATH = "E:\\dataset\\NCKU\\Lung\\{}\\".format(MODE)
GROUNDTRUTH_PATH = "E:\\dataset\\NCKU\\Lung\\label\\"


def evaluate_model(model_path, mode):

    def accuracy(count):
        TP = count[1, 1]
        TN = count[0, 0]
        FP = count[1, 0]
        FN = count[0, 1]

        recall    = 1 if TP == FN == 0 else TP / (TP + FN)
        precision = 1 if TP == FP == 0 else TP / (TP + FP)

        return recall, precision


    result_path = os.path.join(model_path.split(".hdf5")[0], mode)
    status = collections.defaultdict(lambda: collections.defaultdict(list))
    for path in glob(os.path.join(result_path, "*")):
        patientID = path.split("patientID=")[1].split(",sliceID")[0]
        for npzfile_heapMap in glob(os.path.join(path, "*.npz")):
            sliceID = npzfile_heapMap[-7:-4]
            status[patientID][sliceID].append(npzfile_heapMap)
    

    for patientID in sorted(status.keys()):

        total_recall = 0
        total_precision = 0
        total_slice = 0

        for sliceID in sorted(status[patientID].keys()):
            heapMap = np.zeros(IMAGE_SPATIAL_DIMS[:-1])
            for npzfile_heapMap_path in status[patientID][sliceID]:
                newHeapMap = np.load(npzfile_heapMap_path)["heapMap"]
                heapMap = np.maximum(heapMap, newHeapMap)
            heapMap = np.where(heapMap > THRESHOLD, 1, 0)

            groundTruth_image_path = os.path.join(GROUNDTRUTH_PATH, "IMG-{}-{}.jpg".format(patientID.zfill(4), sliceID.zfill(5)))
            # print(groundTruth_image_path)
            if os.path.exists(groundTruth_image_path):
                groundTruth_image = cv2.imread(groundTruth_image_path, 0)
                groundTruth_image = np.where(groundTruth_image > 125, 1, 0)
                # count = collections.Counter(groundTruth_image.flatten())
                # print("status = {}".format(str(count)))
            else:
                groundTruth_image = np.zeros(IMAGE_SPATIAL_DIMS[:-1])

            count = collections.Counter([(int(img), int(gt)) for img, gt in zip(heapMap.flatten(), groundTruth_image.flatten())])

            recall, precision = accuracy(count)
            total_recall += recall
            total_precision += precision
            total_slice += 1

        print("patientID = {}, recall = {}, precision = {}".format(patientID, total_recall / total_slice, total_precision / total_slice))


def predict_model(model_path, mode):

    def transfer(image):
        image = np.squeeze(image, axis =  0)
        image = np.squeeze(image, axis = -1)
        image = image.transpose((2, 0, 1))
        return image

    model = getModel3(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, model_path)

    for datas, sliceIDList, patientID in getInferenceGenerator(DATA_PATH):

        startSliceID, endSliceID = str(sliceIDList[0]).zfill(3), str(sliceIDList[-1]).zfill(3)
        if int(patientID) < 499:
            print("patientID = {} skip !!!".format(patientID))
            continue

        outputs = model(datas)

        print("====================== patientID = {}, sliceID = {} ~ {} (max score = {}) ======================".format(patientID, startSliceID, endSliceID, np.max(outputs)))

        heapMaps   = transfer(outputs)
        
        binaryMaps = np.where(outputs > THRESHOLD, 255, 0)
        binaryMaps = np.array(binaryMaps, int)
        binaryMaps = transfer(binaryMaps)

        count = collections.Counter(binaryMaps.flatten())
        print("status = {}".format(str(count)))
        
        save_path = os.path.join(model_path.split(".hdf5")[0], mode, "patientID={},sliceID={}~{}".format(patientID, startSliceID, endSliceID))

        for heapMap, binaryMap, sliceID in zip(heapMaps, binaryMaps, sliceIDList):
            npzfile_heapMap = "npzfile_heapMap,patientID={},sliceID={}.npz".format(patientID, str(sliceID).zfill(3))
            heapMap_name = "heapMap,patientID={},sliceID={}.jpg".format(patientID, str(sliceID).zfill(3))
            binaryMap_name = "binaryMap,patientID={},sliceID={}.jpg".format(patientID, str(sliceID).zfill(3))
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            npzfile_heapMap_save_path = os.path.join(save_path, npzfile_heapMap)
            # if not os.path.exists(npzfile_heapMap_save_path):
            np.savez(npzfile_heapMap_save_path, heapMap = heapMap)

            heapMap_save_path = os.path.join(save_path, heapMap_name)
            # if not os.path.exists(heapMap_save_path):
            plt.clf()
            plt.imshow(heapMap, cmap = "hot", vmin = 0, vmax = 1)
            plt.colorbar()
            plt.savefig(heapMap_save_path)

            binaryMap_save_path = os.path.join(save_path, binaryMap_name)
            # if not os.path.exists(binaryMap_save_path):
            cv2.imwrite(binaryMap_save_path, binaryMap)

def test():
    model_path = os.path.join(SAVE_PATH, MODEL_NAME)
    # predict_model(model_path, MODE)
    evaluate_model(model_path, MODE)


if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    test()

