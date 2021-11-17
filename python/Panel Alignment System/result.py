import cv2
import numpy as np
import json
from glob import glob

from numpy.lib.function_base import diff

# index = 0

# path1 = ".\Test Image_20210913\M3mm_Deg1_Bri255\cal_{}_L.png".format(index)
# path2 = ".\Test Image_20210913\M3mm_Deg2.5_Bri255\cal_{}_L.png".format(index)

# image1 = cv2.imread(path1, 0)
# image2 = cv2.imread(path2, 0)

# shape = np.shape(image1)
# diff = np.sum(image1 - image2) / (shape[0] * shape[1])

# print(diff)
# print(image1 - image2)


def cal_difference(path, index):
    start, end = index

    f = open(path + "result.txt", "r")
    content = f.readlines()
    content = "".join(content)

    L_table, R_table = [], []
    for index in range(start, end + 1):
        str_ = content.split("cal_{}_{}: ".format(index, "L"))[-1].split("\n")[0]
        x = int(str_.split(",")[0].split("x = ")[-1])
        y = int(str_.split(", y = ")[-1])
        L_table += [(x, y)]

    for index in range(start, end + 1):
        str_ = content.split("cal_{}_{}: ".format(index, "R"))[-1].split("\n")[0]
        x = int(str_.split(",")[0].split("x = ")[-1])
        y = int(str_.split(", y = ")[-1])
        R_table += [(x, y)]

    # answer
    L_answer_table, R_answer_table = [], []
    for index in range(start, end + 1):
        f = open(path + "cal_{}_L.json".format(index), "r")
        data = json.load(f)

        x = int(data["shapes"][3]["points"][0][0])
        y = int(data["shapes"][3]["points"][0][1])
        L_answer_table += [(x, y)]

    for index in range(start, end + 1):
        f = open(path + "cal_{}_R.json".format(index), "r")
        data = json.load(f)

        x = int(data["shapes"][3]["points"][0][0]) - 200
        y = int(data["shapes"][3]["points"][0][1])
        R_answer_table += [(x, y)]

    # diff
    diff_L, diff_R = [], []
    for index in range(len(L_answer_table)):
        x, y = L_table[index]
        _x, _y = L_answer_table[index]
        diff_L.append(((x - _x) ** 2 + (y - _y) ** 2) ** 0.5)

    for index in range(len(R_answer_table)):
        x, y = R_table[index]
        _x, _y = R_answer_table[index]
        diff_R.append(((x - _x) ** 2 + (y - _y) ** 2) ** 0.5)
        
    return np.mean(diff_L), np.mean(diff_R)



paths = glob(".\Test Image_20210913\M3mm_Deg*")
# paths = [".\Test Image_20210913\M3mm_Deg1_Bri30\\"]

for path in paths:
    path += "\\"
    diff_translation = np.mean(cal_difference(path, [0, 8]))
    diff_rotation = np.mean(cal_difference(path, [9, 10]))
    print(path)
    print("diff_translation", round(diff_translation, 2))
    print("diff_rotation", round(diff_rotation, 2))
    print("=================================")

    