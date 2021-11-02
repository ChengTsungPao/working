import cv2
import copy
import numpy as np
from calculate import getAngleMagnitude, getGradient

class imageProcessing():

    def __init__(self):
        self.image = []
        self.imageType = ""
        self.resetImage()


    def resetImage(self):
        self.cropResizeImage = []
        self.canny = []
        self.contour = []
        self.contours = []
        self.drawContour = []
        self.index = 0

        self.Gradient = []
        self.magnitude = []
        self.angle = []


    def setImage(self, image, imageType):
        self.image = image
        self.imageType = imageType
        self.resetImage()


    def cropImageResize(self):
        if self.image == []:
            return

        x = 0 if self.imageType == "L" else 200
        y = 0

        w = 1080
        h = 660

        imageTemp = self.image[y : y + h , x : x + w]
        shape = np.shape(imageTemp)
        self.cropResizeImage = cv2.resize(imageTemp, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)
        self.cropResizeImage = imageTemp


    def cannyFilter(self):
        self.resetImage()
        self.cropImageResize()
            
        imageTemp = cv2.GaussianBlur(self.cropResizeImage, (3, 3), 0)
        self.canny = cv2.Canny(imageTemp, 70, 130)


    def findContour(self):
        if self.canny == []:
            self.cannyFilter()
        
        self.contours, hierarchy = cv2.findContours(self.canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.index = self.index - 1 if abs(self.index - 1) <= len(self.contours) else -1
        self.contour = self.contours[self.index]
        self.drawContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.copy(self.contour), -1, (0, 255, 255), 1)


    def calculateData(self):
        if self.contour == []:
            self.findContour()

        self.Gradient, self.orderContour = getGradient(self.cropResizeImage, self.contour, self.imageType)
        self.magnitude, self.angle = getAngleMagnitude(self.Gradient, self.imageType)


    # remove maybe not use
    def sobelfilter(self):

        gray = cv2.cvtColor(self.cropResizeImage, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
        sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)

        x = cv2.convertScaleAbs(sobelx)   
        y = cv2.convertScaleAbs(sobely)

        self.sobelImage = cv2.addWeighted(x,0.5,y,0.5,0)
