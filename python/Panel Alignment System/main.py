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

    def createFile(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def mergeFolder(folders):
        path = ""
        for folder in folders:
            path += folder + "/"
        return path

    image_processing_fcn = imageProcessing()
    paths = glob("./Test Image_20210913/M3mm*")
    # paths = ["./Test Image_20210913\\M3mm_Deg2.5_Bri150"]
    for path in paths:
        light = int(path.split("Bri")[-1])
        path += "//"
        files = os.listdir(path)
        files = glob(path + "cal_*_L.png") + glob(path + "cal_*_R.png")
        for file_ in files:
            try:
                pathfolder = mergeFolder(file_.split("\\")[:-1])
                filename = file_.split("\\")[-1]


                image = cv2.imread(file_)
                imageType = file_.split("/")[-1].split(".png")[-2][-1]
                filename = filename.split(".png")[0]


                createFile(pathfolder + "canny/")
                image_processing_fcn.setImage(image, imageType)
                image_processing_fcn.cropImageResize()
                image_processing_fcn.cannyFilter()
                cv2.imwrite(pathfolder + "canny/" + filename + "_canny.png", image_processing_fcn.canny)


                createFile(pathfolder + "contour/")
                image_processing_fcn.findContour()
                cv2.imwrite(pathfolder + "contour/" + filename + "_contour.png", image_processing_fcn.drawContour)

                createFile(pathfolder + "findContour/")
                image_processing_fcn.houghLinesP()
                cv2.imwrite(pathfolder + "findContour/" + filename + "_findContour.png", image_processing_fcn.drawFindContour)

                image_processing_fcn.calculateData(pathfolder, filename)
                drawContour = image_processing_fcn.drawContour
                Gradient, magnitude, angle, orderContour = image_processing_fcn.Gradient, image_processing_fcn.magnitude, image_processing_fcn.angle, image_processing_fcn.orderContour

                Gradient = [Gradient[index] + (int(index),) for index in range(len(Gradient))]
                candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1], int)
                angle = np.array(angle)


                createFile(pathfolder + "Gradient/")
                Gradient = np.array(Gradient)
                plotResult("Gradient", "index of point", "Gradient", "Gx", np.abs(Gradient[:, 0]))
                plotResult("Gradient", "index of point", "Gradient", "Gy", np.abs(Gradient[:, 1]))
                plt.savefig(pathfolder + "Gradient/" + filename + "_Gradient.png")
                plt.clf()


                createFile(pathfolder + "magnitude/")
                plotResult("magnitude", "index of point", "magnitude", "magnitude", magnitude)
                plt.savefig(pathfolder + "magnitude/" + filename + "_magnitude.png")
                plt.clf()


                createFile(pathfolder + "Angle/")
                plotResult("Angle", "index of point", "degree", "Angle", angle)
                plt.plot(candidate[:, 2], angle[candidate[:, 2]], "o", label = "candidate")
                plt.savefig(pathfolder + "Angle/" + filename + "_Angle.png")
                plt.clf()


                createFile(pathfolder + "result/")
                rad = 8
                point = orderContour[candidate[0][2]]
                cv2.line(drawContour, (point[0] - rad , point[1] - rad), (point[0] + rad, point[1] + rad), (255, 0, 0), 5)
                cv2.line(drawContour, (point[0] - rad , point[1] + rad), (point[0] + rad, point[1] - rad), (255, 0, 0), 5)
                cv2.imwrite(pathfolder + "result/" + filename + "_result.png", drawContour)
            except:
                print(file_)