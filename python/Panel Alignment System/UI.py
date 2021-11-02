from imageProcessing import imageProcessing
from plot import plotResult, drawImage

import tkinter as tk
from tkinter import filedialog
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import matplotlib.pylab as plt
import numpy as np
import cv2

class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        self.image_processing_fcn = imageProcessing()

        self.image = []

        self.cannyButton.clicked.connect(self.cannyEdge)
        self.findContoursButton.clicked.connect(self.findContours)
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

            self.image_processing_fcn.setImage(self.image, self.imageType)

            self.originImageLabel.setPixmap(QPixmap(self.path))
            self.originImageLabel.setScaledContents(True)
            self.originImageLabel.setAlignment(Qt.AlignCenter)


    def cannyEdge(self):
        if self.image == []:
            return

        self.image_processing_fcn.cropImageResize()
        self.image_processing_fcn.cannyFilter()

        path = self.path.split(".png")[0] + "_canny.png"
        cv2.imwrite(path, self.image_processing_fcn.canny)

        self.image = cv2.imread(path)
        self.originImageLabel.setPixmap(QPixmap(path))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)


    def findContours(self):
        if self.image == []:
            return
        
        self.image_processing_fcn.findContour()

        path = self.path.split(".png")[0] + "_contour.png"
        cv2.imwrite(path, self.image_processing_fcn.drawContour)

        self.image = cv2.imread(path)
        self.originImageLabel.setPixmap(QPixmap(path))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)


    def calculate(self):
        if self.image == []:
            return

        self.image_processing_fcn.calculateData()

        canny, drawContour, cropResizeImage = self.image_processing_fcn.canny, self.image_processing_fcn.drawContour, self.image_processing_fcn.cropResizeImage
        Gradient, magnitude, angle, orderContour = self.image_processing_fcn.Gradient, self.image_processing_fcn.magnitude, self.image_processing_fcn.angle, self.image_processing_fcn.orderContour


        Gradient = [Gradient[index] + (int(index),) for index in range(len(Gradient))]
        candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1], int)
        angle = np.array(angle)

        path = self.path.split(".png")[0] 
        
        Gradient = np.array(Gradient)
        plotResult("Gradient", "index of point", "Gradient", "Gx", np.abs(Gradient[:, 0]))
        plotResult("Gradient", "index of point", "Gradient", "Gy", np.abs(Gradient[:, 1]))
        plt.savefig(path + "_Gradient.png")
        plt.clf()

        plotResult("magnitude", "index of point", "magnitude", "magnitude", magnitude)
        plt.savefig(path + "_magnitude.png")
        plt.clf()

        plotResult("Angle", "index of point", "degree", "Angle", angle)
        plt.plot(candidate[:, 2], angle[candidate[:, 2]], "o", label = "candidate")
        plt.savefig(path + "_Angle.png")
        plt.clf()

        rad = 8
        point = orderContour[candidate[0][2]]
        cv2.line(drawContour, (point[0] - rad , point[1] - rad), (point[0] + rad, point[1] + rad), (255, 0, 0), 5)
        cv2.line(drawContour, (point[0] - rad , point[1] + rad), (point[0] + rad, point[1] - rad), (255, 0, 0), 5)
        cv2.imwrite(path + "_result.png", drawContour)

        self.originImageLabel.setPixmap(QPixmap(path + "_result.png"))
        self.originImageLabel.setScaledContents(True)
        self.originImageLabel.setAlignment(Qt.AlignCenter)  

        self.resultImageLabel.setPixmap(QPixmap(path + "_Gradient.png"))
        self.resultImageLabel.setScaledContents(True)
        self.resultImageLabel.setAlignment(Qt.AlignCenter)

        self.plotMagnitudeLabel.setPixmap(QPixmap(path + "_magnitude.png"))
        self.plotMagnitudeLabel.setScaledContents(True)
        self.plotMagnitudeLabel.setAlignment(Qt.AlignCenter)

        self.plotAngleLabel.setPixmap(QPixmap(path + "_Angle.png"))
        self.plotAngleLabel.setScaledContents(True)
        self.plotAngleLabel.setAlignment(Qt.AlignCenter)  