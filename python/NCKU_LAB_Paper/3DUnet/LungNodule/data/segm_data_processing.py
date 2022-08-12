from glob import glob
import numpy as np
import os
import cv2
import random

def getGernerator(data_path, target_path, batch_size = 1, stride = 16, shape = (512, 512, 32)):
    image_paths  = glob(os.path.join(data_path, "*"))
    target_paths = glob(os.path.join(target_path, "*.jpg"))

    target_paths_status = {}
    for target_path in target_paths:
        filename = target_path.split("\\")[-1]
        patientID, sliceID = filename.split("-")[-2], filename.split("-")[-1].split(".jpg")[0]
        patientID, sliceID = int(patientID), int(sliceID)
        target_paths_status[patientID, sliceID] = target_path
    
    # Need To Include Epoch
    while True:
        depth = shape[-1]
        random.shuffle(image_paths)
        for image_path in image_paths:
            patientID = image_path.split("\\")[-1]
            patientID = int(patientID)
            images = np.load(os.path.join(image_path, "{}.npz".format(str(patientID).zfill(4))))["image"]
            number_of_slice = images.shape[1]

            # Notice: batch need to smaller than number of one patient images, batch size = 1
            sliceIDList = list(range(0, number_of_slice, stride))
            random.shuffle(sliceIDList)

            b = 0
            while sliceIDList:
                if b == 0:
                    datas   = np.zeros((batch_size, shape[-1]) + shape[:-1])
                    targets = np.zeros((batch_size, shape[-1]) + shape[:-1])

                while b < batch_size and sliceIDList:
                    sliceIDStart = sliceIDList.pop()
                    if sliceIDStart + depth < number_of_slice:
                        if not any([(patientID, sliceID) in target_paths_status for sliceID in range(sliceIDStart, sliceIDStart + depth)]):
                            continue

                        datas[b]   = images[0][sliceIDStart: sliceIDStart + depth]
                        targets[b] = np.array([cv2.imread(target_paths_status[patientID, sliceID], 0) if (patientID, sliceID) in target_paths_status else np.zeros(shape[:-1]) for sliceID in range(sliceIDStart, sliceIDStart + depth)])
                    else:
                        if not any([(patientID, sliceID) in target_paths_status for sliceID in range(number_of_slice - depth, number_of_slice)]):
                            continue

                        datas[b]   = images[0][number_of_slice - depth:]
                        targets[b] = np.array([cv2.imread(target_paths_status[patientID, sliceID], 0) if (patientID, sliceID) in target_paths_status else np.zeros(shape[:-1]) for sliceID in range(number_of_slice - depth, number_of_slice)])
                    b += 1

                if b >= batch_size:
                    b = 0
                    datas   = np.expand_dims(  datas.transpose((0, 2, 3, 1)), -1) / 255.
                    targets = np.expand_dims(targets.transpose((0, 2, 3, 1)), -1) / 255.
                    yield datas, targets


def getInferenceGenerator(data_path, stride = 16, shape = (512, 512, 32)):
    image_paths  = glob(os.path.join(data_path, "[0-9]*"))
    image_paths.sort()
    
    depth = shape[-1]
    for image_path in image_paths:
        patientID = image_path.split("\\")[-1]
        images = np.load(os.path.join(image_path, "{}.npz".format(str(patientID).zfill(4))))["image"]
        number_of_slice = images.shape[1]

        for sliceIDStart in range(0, number_of_slice, stride):
            if sliceIDStart + depth < number_of_slice:
                sliceIDList = list(range(sliceIDStart, sliceIDStart + depth))
                datas = images[:, sliceIDStart: sliceIDStart + depth, :, :]
            else:
                sliceIDList = list(range(number_of_slice - depth, number_of_slice))
                datas = images[:, number_of_slice - depth:, :, :]

            datas = np.expand_dims(datas.transpose((0, 2, 3, 1)), -1) / 255.
            yield datas, sliceIDList, patientID
            


    


