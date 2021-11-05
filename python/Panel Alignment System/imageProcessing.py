import cv2
import copy
import numpy as np
from numpy.core.fromnumeric import shape
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
        self.drawFindContour = []
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
        self.cropResizeImage = imageTemp
        # shape = np.shape(imageTemp)
        # self.cropResizeImage = cv2.resize(imageTemp, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)


    def cannyFilter(self):
        self.resetImage()
        self.cropImageResize()
            
        imageTemp = cv2.medianBlur(self.cropResizeImage, 5)
        imageTemp = cv2.GaussianBlur(imageTemp, (3, 3), 0)
        self.canny = cv2.Canny(imageTemp, 80, 130)


    def findContour(self):
        if self.canny == []:
            self.cannyFilter()
        
        self.contours, hierarchy = cv2.findContours(self.canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.drawContour = copy.deepcopy(self.cropResizeImage)
        for index in range(len(self.contours)):
            self.drawContour = cv2.drawContours(self.drawContour, copy.copy(self.contours[index]), -1, (0, 255, 255), 3)


    def houghLinesP(self, auto = True):

        def distance(pos1, pos2):
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

        if auto:
            ############################################ use houghLinesP detect contour ####################################################
            contour_index = -1
            maxLength = -float("inf")
            maxLengthLines = []
            shape = np.shape(self.cropResizeImage)

            minLineLength = 100
            maxLineGap = 1

            for index in range(len(self.contours)):

                image = np.zeros(shape)
                image = cv2.drawContours(image, copy.copy(self.contours[index]), -1, (255, 255, 255), 2)

                gray = cv2.cvtColor(np.array(image).astype(np.uint8) , cv2.COLOR_BGR2GRAY)
                image = cv2.cvtColor(gray , cv2.COLOR_BGR2RGB)
                lines = cv2.HoughLinesP(gray, 1, np.pi/180, 100, minLineLength, maxLineGap)

                if np.array([lines == None]).any():
                    continue
                else:
                    lines = sorted(lines, key = lambda x: (x[0][0] - x[0][2]) ** 2 + (x[0][1] - x[0][3]) ** 2, reverse = True)

                length = 0
                for line in lines[:2]:
                    x1, y1, x2, y2 = line[0]
                    length += distance((x1, y1), (x2, y2))
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

                if maxLength < length:
                    contour_index = index
                    maxLengthLines = copy.deepcopy(lines[:2])

            self.contour = self.contours[contour_index]
            image = cv2.drawContours(image, copy.copy(self.contour) , -1, (255, 255, 255), 2)
            self.drawFindContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.copy(self.contour), -1, (0, 255, 255), 3)
            
            if maxLengthLines != []:
                for line in maxLengthLines:
                    x1, y1, x2, y2 = line[0]
                    length += distance((x1, y1), (x2, y2))
                    cv2.line(self.drawFindContour, (x1, y1), (x2, y2), (0, 255, 0), 3)

        else:
            ############################################ click and change contour ####################################################
            self.contours.sort(key = len)
            self.index = self.index - 1 if abs(self.index - 1) <= len(self.contours) else -1
            self.contour = self.contours[self.index]
            self.drawFindContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.copy(self.contour), -1, (0, 255, 255), 3)


    def calculateData(self):
        if self.contour == []:
            self.findContour()
            self.houghLinesP()

        self.Gradient, self.orderContour = getGradient(self.cropResizeImage, self.contour, self.imageType)
        self.magnitude, self.angle = getAngleMagnitude(self.Gradient, self.imageType)

    
    def show_image(self, image, title = "test"):
        cv2.imshow(title, image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 


    # remove maybe not use
    def sobelfilter(self):
    
        gray = cv2.cvtColor(self.cropResizeImage, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
        sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)

        x = cv2.convertScaleAbs(sobelx)   
        y = cv2.convertScaleAbs(sobely)

        self.sobelImage = cv2.addWeighted(x,0.5,y,0.5,0)
