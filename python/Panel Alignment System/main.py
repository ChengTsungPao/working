import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    # app = QtWidgets.QApplication(sys.argv)
    # ui = UI()
    # sys.exit(app.exec_())

    from imageProcessing import imageProcessing
    from plot import plotResult, drawImage
    from glob import glob
    import matplotlib.pylab as plt
    import numpy as np
    import os
    import cv2

    # def createFile(path):
    #     if not os.path.exists(path):
    #         os.makedirs(path)

    # image_processing_fcn = imageProcessing()
    # paths = glob("./Test Image_20210913/M3mm*")
    # paths = ["./Test Image_20210913\\M3mm_Deg2.5_Bri150"]
    # for path in paths:
    #     light = int(path.split("Bri")[-1])
    #     path += "//"
    #     files = os.listdir(path)
    #     files = glob(path + "cal_*_L.png") + glob(path + "cal_*_R.png")
    #     for file_ in files:
    #         print(file_)
    #         print(file_.split("\\"))
    #         break

            # image = cv2.imread(file_)
            # imageType = file_.split("/")[-1].split(".png")[-2][-1]
            # path = file_.split(".png")[0]


            # createFile(path)
            # image_processing_fcn.setImage(image, imageType)
            # image_processing_fcn.cropImageResize()
            # image_processing_fcn.cannyFilter()
            # cv2.imwrite(path + "_canny.png", image_processing_fcn.canny)


            # createFile(path)
            # image_processing_fcn.findContour()
            # cv2.imwrite(path + "_contour.png", image_processing_fcn.drawContour)

            # image_processing_fcn.calculateData()
            # canny, drawContour, cropResizeImage = image_processing_fcn.canny, image_processing_fcn.drawContour, image_processing_fcn.cropResizeImage
            # Gradient, magnitude, angle, orderContour = image_processing_fcn.Gradient, image_processing_fcn.magnitude, image_processing_fcn.angle, image_processing_fcn.orderContour

            # Gradient = [Gradient[index] + (int(index),) for index in range(len(Gradient))]
            # candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1], int)
            # angle = np.array(angle)


            # createFile(path)
            # Gradient = np.array(Gradient)
            # plotResult("Gradient", "index of point", "Gradient", "Gx", np.abs(Gradient[:, 0]))
            # plotResult("Gradient", "index of point", "Gradient", "Gy", np.abs(Gradient[:, 1]))
            # plt.savefig(path + "_Gradient.png")
            # plt.clf()


            # createFile(path)
            # plotResult("magnitude", "index of point", "magnitude", "magnitude", magnitude)
            # plt.savefig(path + "_magnitude.png")
            # plt.clf()


            # createFile(path)
            # plotResult("Angle", "index of point", "degree", "Angle", angle)
            # plt.plot(candidate[:, 2], angle[candidate[:, 2]], "o", label = "candidate")
            # plt.savefig(path + "_Angle.png")
            # plt.clf()


            # createFile(path)
            # rad = 8
            # point = orderContour[candidate[0][2]]
            # cv2.line(drawContour, (point[0] - rad , point[1] - rad), (point[0] + rad, point[1] + rad), (255, 0, 0), 5)
            # cv2.line(drawContour, (point[0] - rad , point[1] + rad), (point[0] + rad, point[1] - rad), (255, 0, 0), 5)
            # cv2.imwrite(path + "_result.png", drawContour)