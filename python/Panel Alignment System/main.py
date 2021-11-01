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

    # paths = glob("./Test Image_20210913/M3mm*")
    # # paths = ["./Test Image_20210913\\M3mm_Deg2.5_Bri150"]
    # for path in paths:
    #     light = int(path.split("Bri")[-1])
    #     path += "//"
    #     files = os.listdir(path)
    #     files = glob(path + "cal_*_L.png") + glob(path + "cal_*_R.png")
    #     for file_ in files:

    #         try:

    #             imageType = file_.split(".png")[0][-1]
    #             image = cv2.imread(file_)
    #             data = imageProcessing(image, light, imageType)
    #             canny, drawContour, cropResizeImage = data["image"]
    #             Gradient, magnitude, angle, contour = data["result"]
    #             cv2.imwrite(file_.split(".png")[0] + "_canny.png", canny)


    #             for index in range(len(Gradient)):
    #                 Gradient[index] += (int(index),)
    #             candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1])
    #             candidate = np.array(candidate, int)
    #             angle = np.array(angle)


    #             Gradient = np.array(Gradient)
    #             plotResult("Gradient", "index of point", "Gradient", "Gx", np.abs(Gradient[:, 0]))
    #             plotResult("Gradient", "index of point", "Gradient", "Gy", np.abs(Gradient[:, 1]))
    #             plt.savefig(file_.split(".png")[0] + "_Gradient.png")
    #             plt.clf()

    #             plotResult("magnitude", "index of point", "magnitude", "magnitude", magnitude)
    #             plt.savefig(file_.split(".png")[0] + "_magnitude.png")
    #             plt.clf()

    #             plotResult("Angle", "index of point", "degree", "Angle", angle)
    #             plt.plot(candidate[:, 2], angle[candidate[:, 2]], "o", label = "candidate")
    #             plt.savefig(file_.split(".png")[0] + "_Angle.png")
    #             plt.clf()

    #             angle_dev = angle[1:] - angle[:-1]
    #             plotResult("Angle_dev", "index of point", "degree", "Angle_dev", angle_dev)
    #             plt.plot(candidate[:, 2], angle_dev[candidate[:, 2]], "o", label = "candidate")
    #             plt.savefig(file_.split(".png")[0] + "_Angle_dev.png")
    #             plt.clf()

    #             point = contour[candidate[0][2]]

    #             rad = 5
    #             cv2.line(drawContour, (point[0] - rad , point[1] - rad), (point[0] + rad, point[1] + rad), (255, 0, 0), 2)
    #             cv2.line(drawContour, (point[0] - rad , point[1] + rad), (point[0] + rad, point[1] - rad), (255, 0, 0), 2)
    #             cv2.imwrite(file_.split(".png")[0] + "_result.png", drawContour)

    #         except:
    #             print(file_)