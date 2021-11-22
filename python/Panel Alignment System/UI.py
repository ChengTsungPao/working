from imageProcessing import imageProcessing
from plot import plotResult, drawImage

import tkinter as tk
from tkinter import filedialog
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import matplotlib.pylab as plt
import numpy as np
import cv2, os

class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        self.image_processing_fcn = imageProcessing()

        self.image = []

        self.cannyButton.clicked.connect(self.cannyEdge)
        self.findContoursButton.clicked.connect(self.findContours)
        self.houghLinesPButton.clicked.connect(self.houghLinesP)
        self.loadButton.clicked.connect(self.loadImage)
        self.calculateButton.clicked.connect(self.calculate)
        self.show()


    def loadImage(self):

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename()

        if path != "":
            self.path = path
            self.image = cv2.imread(self.path)
            self.imageType = self.path.split("/")[-1].split(".png")[-2][-1]

            self.pathFolder = self.mergeFolder(self.path.split("/")[:-1])
            self.filename = self.path.split("/")[-1].split(".png")[0]

            self.image_processing_fcn.setImage(self.image, self.imageType)

            self.originImageLabel.setPixmap(QPixmap(self.path))
            self.originImageLabel.setScaledContents(True)
            self.originImageLabel.setAlignment(Qt.AlignCenter)


    def cannyEdge(self):
        if self.image == []:
            return

        self.image_processing_fcn.cropImageResize()
        self.image_processing_fcn.cannyFilter()

        self.createFile(self.pathFolder + "canny/")
        cv2.imwrite(self.pathFolder + "canny/" + self.filename + "_canny.png", self.image_processing_fcn.canny)        

        self.image = cv2.imread(self.pathFolder + "canny/" + self.filename + "_canny.png")
        self.originImageLabel.setPixmap(QPixmap(self.pathFolder + "canny/" + self.filename + "_canny.png"))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)


    def findContours(self):
        if self.image == []:
            return
        
        self.image_processing_fcn.findContour()

        self.createFile(self.pathFolder + "contour/")
        cv2.imwrite(self.pathFolder + "contour/" + self.filename + "_contour.png", self.image_processing_fcn.drawContour)

        self.image = cv2.imread(self.pathFolder + "contour/" + self.filename + "_contour.png")
        self.originImageLabel.setPixmap(QPixmap(self.pathFolder + "contour/" + self.filename + "_contour.png"))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)


    def houghLinesP(self):
        if self.image == []:
            return

        self.image_processing_fcn.houghLinesP(self.findContourAutoCheckBox.isChecked())

        self.createFile(self.pathFolder + "findContour/")
        cv2.imwrite(self.pathFolder + "findContour/" + self.filename + "_findContour.png", self.image_processing_fcn.drawFindContour)

        self.image = cv2.imread(self.pathFolder + "findContour/" + self.filename + "_findContour.png")
        self.originImageLabel.setPixmap(QPixmap(self.pathFolder + "findContour/" + self.filename + "_findContour.png"))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)


    def calculate(self):
        if self.image == []:
            return

        self.image_processing_fcn.calculateData()

        canny, drawContour, drawFindContour, cropResizeImage = self.image_processing_fcn.canny, self.image_processing_fcn.drawContour, self.image_processing_fcn.drawFindContour, self.image_processing_fcn.cropResizeImage
        Gradient, magnitude, angle, orderContour = self.image_processing_fcn.Gradient, self.image_processing_fcn.magnitude, self.image_processing_fcn.angle, self.image_processing_fcn.orderContour


        Gradient = [Gradient[index] + (int(index),) for index in range(len(Gradient))]
        candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1], int)
        angle = np.array(angle)

        self.createFile(self.pathFolder + "Gradient/")
        self.createFile(self.pathFolder + "magnitude/")
        self.createFile(self.pathFolder + "Angle/")
        self.createFile(self.pathFolder + "result/")

        Gradient = np.array(Gradient)
        plotResult("Gradient", "index of point", "Gradient", "Gx", np.abs(Gradient[:, 0]))
        plotResult("Gradient", "index of point", "Gradient", "Gy", np.abs(Gradient[:, 1]))
        plt.savefig(self.pathFolder + "Gradient/" + self.filename + "_Gradient.png")
        plt.clf()

        plotResult("magnitude", "index of point", "magnitude", "magnitude", magnitude)
        plt.savefig(self.pathFolder + "magnitude/" + self.filename + "_magnitude.png")
        plt.clf()

        plotResult("Angle", "index of point", "degree", "Angle", angle)
        plt.plot(candidate[:, 2], angle[candidate[:, 2]], "o", label = "candidate")
        plt.savefig(self.pathFolder + "Angle/" + self.filename + "_Angle.png")
        plt.clf()

        rad = 8
        point = orderContour[candidate[0][2]]
        cv2.line(drawContour, (point[0] - rad , point[1] - rad), (point[0] + rad, point[1] + rad), (0, 255, 0), 2)
        cv2.line(drawContour, (point[0] - rad , point[1] + rad), (point[0] + rad, point[1] - rad), (0, 255, 0), 2)

        import json
        f = open(self.pathFolder + self.filename + ".json", "r")
        data = json.load(f)
        x = int(data["shapes"][3]["points"][0][0]) - (200 if self.imageType == "R" else 0)
        y = int(data["shapes"][3]["points"][0][1])
        # x, y = y, x
        cv2.line(drawContour, (x - rad , y - rad), (x + rad, y + rad), (255, 0, 0), 5)
        cv2.line(drawContour, (x - rad , y + rad), (x + rad, y - rad), (255, 0, 0), 5)

        cv2.imwrite(self.pathFolder + "result/" + self.filename + "_result.png", drawContour)
        # self.show_image(drawContour)

        self.originImageLabel.setPixmap(QPixmap(self.pathFolder + "result/" + self.filename + "_result.png"))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)  

        self.resultImageLabel.setPixmap(QPixmap(self.pathFolder + "Gradient/" + self.filename + "_Gradient.png"))
        self.resultImageLabel.setScaledContents(True)
        self.resultImageLabel.setAlignment(Qt.AlignCenter)

        self.plotMagnitudeLabel.setPixmap(QPixmap(self.pathFolder + "magnitude/" + self.filename + "_magnitude.png"))
        self.plotMagnitudeLabel.setScaledContents(True)
        self.plotMagnitudeLabel.setAlignment(Qt.AlignCenter)

        self.plotAngleLabel.setPixmap(QPixmap(self.pathFolder + "Angle/" + self.filename + "_Angle.png"))
        self.plotAngleLabel.setScaledContents(True)
        self.plotAngleLabel.setAlignment(Qt.AlignCenter)  


    def createFile(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def show_image(self, image, title = "test"):
        cv2.imshow(title, image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 

    def mergeFolder(self, folders):
        path = ""
        for folder in folders:
            path += folder + "/"

        return path