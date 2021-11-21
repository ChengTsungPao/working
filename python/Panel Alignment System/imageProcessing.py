import cv2
import copy
import numpy as np
from numpy.core.fromnumeric import shape
from calculate import getAngleMagnitude, getGradient, transferContour

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
        self.smoothImage = copy.deepcopy(imageTemp)
        self.canny = cv2.Canny(imageTemp, 80, 130)


    def findContour(self):
        if self.canny == []:
            self.cannyFilter()
        
        self.contours, hierarchy = cv2.findContours(self.canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.contours.sort(key = len)
        self.drawContour = copy.deepcopy(self.cropResizeImage)
        for index in range(len(self.contours)):
            self.drawContour = cv2.drawContours(self.drawContour, copy.copy(self.contours[index]), -1, (0, 255, 255), 3)


    def houghLinesPHandler(self, lines):

        minLengthLinesScale = 1 / 4
        minTwoLinesAngle = np.pi / 4

        x1, y1, x2, y2 = lines[0][0]
        vector1 = np.array([x1 - x2, y1 - y2])
        length1 = np.linalg.norm(vector1)
        vector1 = vector1 / length1

        choose = [[lines[0][0]]]
        bestLength = length1 * minLengthLinesScale
        bestInnerProduct = float("inf")

        for line in lines[1:]:
            x1, y1, x2, y2 = line[0]
            vector2 = np.array([x1 - x2, y1 - y2])
            length2 = np.linalg.norm(vector2)
            vector2 = vector2 / length2

            innerProduct = abs(np.dot(vector1, vector2))
            if length2 > bestLength and innerProduct < abs(np.cos(minTwoLinesAngle)) and innerProduct < bestInnerProduct:
                bestInnerProduct = abs(np.dot(vector1, vector2))
                bestLength = length2
                if len(choose) == 2:
                    choose[-1] = [line[0].copy()]
                else:
                    choose.append([line[0].copy()])

        return choose, len(choose) == 2


    def houghLinesP(self, auto = True):
        if self.canny == []:
            self.cannyFilter()
            self.findContour()

        def distance(pos1, pos2):
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

        if auto:
            ############################################ use houghLinesP detect contour ####################################################
            contour_index = -1
            maxLength = -float("inf")
            maxLengthLines = []
            shape = np.shape(self.cropResizeImage)

            minLineLength = 10
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
                    lines, isVertical = self.houghLinesPHandler(lines)
                    if isVertical == False: continue

                length = 0
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    length += distance((x1, y1), (x2, y2))
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

                if maxLength < length:
                    contour_index = index
                    maxLength = length
                    maxLengthLines = copy.deepcopy(lines[:2])

            self.contour = self.contours[contour_index]
            image = cv2.drawContours(image, copy.copy(self.contour) , -1, (255, 255, 255), 2)
            self.orderContour = transferContour(np.shape(self.smoothImage), self.contour, self.imageType)
            self.drawFindContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.deepcopy(self.transferSize(self.orderContour)), -1, (0, 255, 255), 3)
            
            if maxLengthLines != []:
                for line in maxLengthLines:
                    x1, y1, x2, y2 = line[0]
                    length += distance((x1, y1), (x2, y2))
                    cv2.line(self.drawFindContour, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    
            self.drawContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.deepcopy(self.transferSize(self.orderContour)), -1, (0, 255, 255), 3)

        else:
            ############################################ click and change contour ####################################################
            self.contours.sort(key = len)
            self.index = self.index - 1 if abs(self.index - 1) <= len(self.contours) else -1
            self.contour = self.contours[self.index]
            self.orderContour = transferContour(np.shape(self.smoothImage), self.contour, self.imageType)
            self.drawFindContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.deepcopy(self.transferSize(self.orderContour)), -1, (0, 255, 255), 3)
            self.drawContour = cv2.drawContours(copy.deepcopy(self.cropResizeImage), copy.deepcopy(self.transferSize(self.orderContour)), -1, (0, 255, 255), 3)


    def calculateData(self, path = "", filename = ""):
        if self.contour == []:
            self.findContour()
            self.houghLinesP()

        self.Gradient = getGradient(self.smoothImage, self.orderContour)
        self.magnitude, self.angle = getAngleMagnitude(self.Gradient, self.imageType)

        Gradient = [self.Gradient[index] + (int(index),) for index in range(len(self.Gradient))]
        candidate = np.array(sorted(Gradient, key = lambda x: abs(abs(x[0]) - abs(x[1])))[:1], int)

        # test = list(self.orderContour)
        # for index in range(len(test)):
        #     test[index] = list(test[index])
        #     test[index].append(index)
        # shape = np.shape(self.cropResizeImage)
        # if self.imageType == "L":
        #     candidate = np.array(sorted(test, key = lambda x: (x[0] - shape[1]) ** 2 + (x[1] - shape[0]) ** 2)[:1], int)
        # else:
        #     candidate = np.array(sorted(test, key = lambda x: (x[0] - shape[1]) ** 2 + (x[1] - 0) ** 2)[:1], int)

        point = self.orderContour[candidate[0][2]]

        if path != "" and filename != "":
            f = open(path + "result.txt", "a")
            f.write("{}: x = {}, y = {}\n".format(filename, point[0], point[1]))
            f.close()

    
    def show_image(self, image, title = "test"):
        cv2.imshow(title, image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 

    
    def transferSize(self, contour):
        newContour = []
        for x in contour:
            newContour.append(np.array([x]))
        return newContour


    # remove maybe not use
    def sobelfilter(self):
    
        gray = cv2.cvtColor(self.cropResizeImage, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
        sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)

        x = cv2.convertScaleAbs(sobelx)   
        y = cv2.convertScaleAbs(sobely)

        self.sobelImage = cv2.addWeighted(x,0.5,y,0.5,0)
