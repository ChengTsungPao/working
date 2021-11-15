import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

    # from imageProcessing import imageProcessing
    # from plot import plotResult, drawImage
    # from glob import glob
    # import matplotlib.pylab as plt
    # import numpy as np
    # import os
    # import cv2
    # import json 

    # def createFile(path):
    #     if not os.path.exists(path):
    #         os.makedirs(path)

    # def mergeFolder(folders):
    #     path = ""
    #     for folder in folders:
    #         path += folder + "/"
    #     return path

    # def create_table(path):
    #     f = open(path + "result.txt", "r")
    #     content = f.readlines()
    #     content = "".join(content)

    #     table = {
    #         0: (1, 1),
    #         1: (1, 2),
    #         2: (0, 2),
    #         3: (0, 1),
    #         4: (0, 0),
    #         5: (1, 0),
    #         6: (2, 0),
    #         7: (2, 1),
    #         8: (2, 2)
    #     }

    #     L_table, R_table = [[""] * 3 for _ in range(3)], [[""] * 3 for _ in range(3)]
    #     for index in range(9):
    #         str_ = content.split("cal_{}_{}: ".format(index, "L"))[-1].split("\n")[0]
    #         x = str_.split(",")[0].split("x = ")[-1]
    #         y = str_.split(", y = ")[-1]
    #         i, j = table[index]
    #         L_table[i][j] = "({}, {})".format(x, y)

    #     for index in range(9):
    #         str_ = content.split("cal_{}_{}: ".format(index, "R"))[-1].split("\n")[0]
    #         x = str_.split(",")[0].split("x = ")[-1]
    #         y = str_.split(", y = ")[-1]
    #         i, j = table[index]
    #         R_table[i][j] = "({}, {})".format(x, y)

    #     plt.title(path.split("\\")[-1].split("//")[0] + "_L")
    #     the_table = plt.table(L_table, loc="center")
    #     the_table.set_fontsize(20)
    #     the_table.scale(1, 7)
    #     plt.axis('off')
    #     plt.axis('tight')
    #     plt.savefig(path + "L_table.png")
    #     # plt.show()
    #     plt.clf()

    #     plt.title(path.split("\\")[-1].split("//")[0] + "_R")
    #     the_table = plt.table(R_table, loc="center")
    #     the_table.scale(1, 7)
    #     the_table.set_fontsize(20)
    #     plt.axis('off')
    #     plt.axis('tight')
    #     plt.savefig(path + "R_table.png")
    #     # plt.show()
    #     plt.clf()

    #     # answer
    #     json_file_fail = False
    #     try:
    #         L_answer_table, R_answer_table = [[""] * 3 for _ in range(3)], [[""] * 3 for _ in range(3)]
    #         for index in range(9):
    #             f = open(path + "cal_{}_L.json".format(index), "r")
    #             data = json.load(f)

    #             x = int(data["shapes"][3]["points"][0][0])
    #             y = int(data["shapes"][3]["points"][0][1])
    #             i, j = table[index]
    #             L_answer_table[i][j] = "({}, {})".format(x, y)

    #         for index in range(9):
    #             f = open(path + "cal_{}_R.json".format(index), "r")
    #             data = json.load(f)

    #             x = int(data["shapes"][3]["points"][0][0]) - 200
    #             y = int(data["shapes"][3]["points"][0][1])
    #             i, j = table[index]
    #             R_answer_table[i][j] = "({}, {})".format(x, y)

    #         plt.title(path.split("\\")[-1].split("//")[0] + "_L_answer")
    #         the_table = plt.table(L_answer_table, loc="center")
    #         the_table.set_fontsize(20)
    #         the_table.scale(1, 7)
    #         plt.axis('off')
    #         plt.axis('tight')
    #         plt.savefig(path + "L_answer_table.png")
    #         # plt.show()
    #         plt.clf()

    #         plt.title(path.split("\\")[-1].split("//")[0] + "_R_answer")
    #         the_table = plt.table(R_answer_table, loc="center")
    #         the_table.scale(1, 7)
    #         the_table.set_fontsize(20)
    #         plt.axis('off')
    #         plt.axis('tight')
    #         plt.savefig(path + "R_answer_table.png")
    #         # plt.show()
    #         plt.clf()
    #     except:
    #         print(path + " do not find .json file")
    #         json_file_fail = True
    #         pass

    #     return json_file_fail

    # def cal_difference(path):
    #     f = open(path + "result.txt", "r")
    #     content = f.readlines()
    #     content = "".join(content)

    #     L_table, R_table = [], []
    #     for index in range(11):
    #         str_ = content.split("cal_{}_{}: ".format(index, "L"))[-1].split("\n")[0]
    #         x = int(str_.split(",")[0].split("x = ")[-1])
    #         y = int(str_.split(", y = ")[-1])
    #         L_table += [(x, y)]

    #     for index in range(11):
    #         str_ = content.split("cal_{}_{}: ".format(index, "R"))[-1].split("\n")[0]
    #         x = int(str_.split(",")[0].split("x = ")[-1])
    #         y = int(str_.split(", y = ")[-1])
    #         R_table += [(x, y)]

    #     # answer
    #     L_answer_table, R_answer_table = [], []
    #     for index in range(11):
    #         f = open(path + "cal_{}_L.json".format(index), "r")
    #         data = json.load(f)

    #         x = int(data["shapes"][3]["points"][0][0])
    #         y = int(data["shapes"][3]["points"][0][1])
    #         L_answer_table += [(x, y)]

    #     for index in range(11):
    #         f = open(path + "cal_{}_R.json".format(index), "r")
    #         data = json.load(f)

    #         x = int(data["shapes"][3]["points"][0][0]) - 200
    #         y = int(data["shapes"][3]["points"][0][1])
    #         R_answer_table += [(x, y)]

    #     # diff
    #     diff_L, diff_R = [], []
    #     for index in range(len(L_answer_table)):
    #         x, y = L_table[index]
    #         _x, _y = L_answer_table[index]
    #         diff_L.append(((x - _x) ** 2 + (y - _y) ** 2) ** 0.5)

    #     for index in range(len(R_answer_table)):
    #         x, y = R_table[index]
    #         _x, _y = R_answer_table[index]
    #         diff_R.append(((x - _x) ** 2 + (y - _y) ** 2) ** 0.5)

    #     return np.mean(diff_L), np.mean(diff_R)


    # image_processing_fcn = imageProcessing()
    # paths = glob("./Test Image_20210913/M3mm*")
    # diff = {"1": {"L": [], "R": []}, "2.5": {"L": [], "R": []}}
    # # paths = ["./Test Image_20210913\\M3mm_Deg1_Bri255"]
    # for path in paths:
    #     light = int(path.split("Bri")[-1])
    #     path += "//"
    #     try:
    #         os.remove(path + "result.txt")
    #     except:
    #         pass
    #     files = os.listdir(path)
    #     files = glob(path + "cal_*_L.png") + glob(path + "cal_*_R.png")

    #     for file_ in files:
    #         try:
    #             pathfolder = mergeFolder(file_.split("\\")[:-1])
    #             filename = file_.split("\\")[-1]


    #             image = cv2.imread(file_)
    #             imageType = file_.split("/")[-1].split(".png")[-2][-1]
    #             filename = filename.split(".png")[0]


    #             createFile(pathfolder + "canny/")
    #             image_processing_fcn.setImage(image, imageType)
    #             image_processing_fcn.cropImageResize()
    #             image_processing_fcn.cannyFilter()
    #             cv2.imwrite(pathfolder + "canny/" + filename + "_canny.png", image_processing_fcn.canny)


    #             createFile(pathfolder + "contour/")
    #             image_processing_fcn.findContour()
    #             cv2.imwrite(pathfolder + "contour/" + filename + "_contour.png", image_processing_fcn.drawContour)

    #             createFile(pathfolder + "findContour/")
    #             image_processing_fcn.houghLinesP()
    #             cv2.imwrite(pathfolder + "findContour/" + filename + "_findContour.png", image_processing_fcn.drawFindContour)

    #             image_processing_fcn.calculateData(pathfolder, filename)
    #             drawContour = image_processing_fcn.drawContour
    #             Gradient, magnitude, angle, orderContour = image_processing_fcn.Gradient, image_processing_fcn.magnitude, image_processing_fcn.angle, image_processing_fcn.orderContour

    #             Gradient = [Gradient[index] + (int(index),) for index in range(len(Gradient))]
    #             candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1], int)
    #             angle = np.array(angle)


    #             createFile(pathfolder + "Gradient/")
    #             Gradient = np.array(Gradient)
    #             plotResult("Gradient", "index of point", "Gradient", "Gx", np.abs(Gradient[:, 0]))
    #             plotResult("Gradient", "index of point", "Gradient", "Gy", np.abs(Gradient[:, 1]))
    #             plt.savefig(pathfolder + "Gradient/" + filename + "_Gradient.png")
    #             plt.clf()


    #             createFile(pathfolder + "magnitude/")
    #             plotResult("magnitude", "index of point", "magnitude", "magnitude", magnitude)
    #             plt.savefig(pathfolder + "magnitude/" + filename + "_magnitude.png")
    #             plt.clf()


    #             createFile(pathfolder + "Angle/")
    #             plotResult("Angle", "index of point", "degree", "Angle", angle)
    #             plt.plot(candidate[:, 2], angle[candidate[:, 2]], "o", label = "candidate")
    #             plt.savefig(pathfolder + "Angle/" + filename + "_Angle.png")
    #             plt.clf()


    #             createFile(pathfolder + "result/")
    #             rad = 8
    #             point = orderContour[candidate[0][2]]
    #             cv2.line(drawContour, (point[0] - rad , point[1] - rad), (point[0] + rad, point[1] + rad), (0, 255, 0), 5)
    #             cv2.line(drawContour, (point[0] - rad , point[1] + rad), (point[0] + rad, point[1] - rad), (0, 255, 0), 5)
    #             cv2.imwrite(pathfolder + "result/" + filename + "_result.png", drawContour)
    #         except:
    #             print(file_)

    #     if create_table(path):
    #         continue

    #     degree = path.split("M3mm_Deg")[-1].split("_Bri")[0]
    #     L_diff, R_diff = cal_difference(path)
    #     diff[degree]["L"].append([int(light), round(L_diff, 2)])
    #     diff[degree]["R"].append([int(light), round(R_diff, 2)])


    # pathResult = "./Test Image_20210913/"
    # for degree in diff.keys():
    #     L_data = np.array(sorted(diff[degree]["L"]))
    #     R_data = np.array(sorted(diff[degree]["R"]))

    #     plt.figure(figsize = (8, 6), dpi = 80)
    #     plt.title("left image degree = {}".format(degree))
    #     plt.plot(L_data[:, 0], L_data[:, 1], "-o")
    #     plt.xlabel("light")
    #     plt.ylabel("mean of difference (pixel)")
    #     plt.savefig(pathResult + "left_image_degree{}.png".format(degree))
    #     # plt.show()
    #     plt.clf()

    #     plt.figure(figsize = (8, 6), dpi = 80)
    #     plt.title("left image table degree = {}".format(degree))
    #     the_table = plt.table(np.array([L_data[:, 0], L_data[:, 1]]), rowLabels=["light","difference"], loc="center")
    #     the_table.scale(1, 6)
    #     the_table.set_fontsize(20)
    #     plt.axis('off')
    #     plt.axis('tight')
    #     plt.savefig(pathResult + "left_image_table_degree{}.png".format(degree))
    #     plt.legend()
    #     # plt.show()
    #     plt.clf()

    #     plt.figure(figsize = (8, 6), dpi = 80)
    #     plt.title("right image degree = {}".format(degree))
    #     plt.plot(R_data[:, 0], R_data[:, 1], "-o")
    #     plt.xlabel("light")
    #     plt.ylabel("mean of difference (pixel)")
    #     plt.savefig(pathResult + "right_image_degree{}.png".format(degree))
    #     # plt.show()
    #     plt.clf()

    #     plt.figure(figsize = (8, 6), dpi = 80)
    #     plt.title("right image table degree = {}".format(degree))
    #     the_table = plt.table(np.array([R_data[:, 0], R_data[:, 1]]), rowLabels=["light","difference"], loc="center")
    #     the_table.scale(1, 6)
    #     the_table.set_fontsize(20)
    #     plt.axis('off')
    #     plt.axis('tight')
    #     plt.legend()
    #     plt.savefig(pathResult + "right_image_table_degree{}.png".format(degree))
    #     # plt.show()
    #     plt.clf()

    



        