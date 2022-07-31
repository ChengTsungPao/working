from operator import mod
import os
from glob import glob
import pandas as pd
import numpy as np
import math
import cv2

def mergeImage(path):
    filenames = sorted(glob(os.path.join(path, "*.jpg")))
    images = []
    for filename in filenames:
        image = cv2.imread(filename, 0)
        if str(image) != "None": images.append(image)
    images = np.array(images, float)
    images = np.expand_dims(images, axis = 0)
    pid = path.split("\\")[-1]
    np.savez(os.path.join(path, "{}.npz".format(pid)), image = images)

def read_image_path(path, mode = "train"):
    return glob(os.path.join(path, mode, "*"))

def read_groundTruth(path, mode = "train", resize = None):
    csv_file = pd.read_csv(os.path.join(path, "{}_anno.csv".format(mode)))
    npz_path = os.path.join(path, mode)

    groundTruth = []
    tlf_points = []
    brb_points = []

    prevPid = csv_file['pid'][0]
    for index in range(len(csv_file['zmin'])):
        pid = csv_file['pid'][index]
        print("\r", "loading data: {} % (pid = {})".format(index * 100 / len(csv_file['zmin']), pid), end=" ")
        image = np.load(os.path.join(npz_path, str(pid).zfill(4), str(pid).zfill(4) + ".npz"))["image"]
        image = image.transpose((0, 2, 3, 1))
        if pid != prevPid:
            groundTruth.append([[tlf_points], [brb_points]])
            tlf_points = []
            brb_points = []

        x1, y1, z1 = csv_file['xmin'][index], csv_file['ymin'][index], csv_file['zmin'][index]
        x2, y2, z2 = csv_file['xmax'][index], csv_file['ymax'][index], csv_file['zmax'][index]
        tlf_points += [[x1, y1, z1]] if resize == None else [[int(x1 * resize[0] / image.shape[1]), int(y1 * resize[1] / image.shape[2]), int(z1 * resize[2] / image.shape[3])]]
        brb_points += [[x2, y2, z2]] if resize == None else [[int(x2 * resize[0] / image.shape[1]), int(y2 * resize[1] / image.shape[2]), int(z2 * resize[2] / image.shape[3])]]
        prevPid = pid

    if tlf_points:
        groundTruth.append([[tlf_points], [brb_points]])
    return groundTruth

if __name__ == "__main__":
    path = "D:\\SANet\\data\\LungNodule\\merge_data"

    points = read_groundTruth(path, mode = "train")
    image_npz_paths = read_image_path(path)
    print(points[0], "=======", points[0][0], "=======", points[0][0][0])
    print(image_npz_paths[0])

    # mergeImage(os.path.join(path, "train", "0448"))