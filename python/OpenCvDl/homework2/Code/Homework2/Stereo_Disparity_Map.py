import cv2
import copy
import numpy as np
import matplotlib.pylab as plt

class stereo_disparity_map():

    def __init__(self, path):
        self.imgLeft = []
        self.imgRight = []
        self.disparity = []
        self.originDisparity = []
        self.path = path

        self.scale = 3
        self.isCal = False


    def setPath(self, path):
        self.path = path 


    def setDisparitySale(self, image):
        return np.array(image / self.scale, int)


    def setImageSize(self, image):
        shape = np.shape(image)
        return cv2.resize(image, (shape[1] // self.scale, shape[0] // self.scale), interpolation=cv2.INTER_AREA)


    def disparity_calculate(self):
        imgLeft = cv2.imread(self.path + 'imL.png')
        imgRight = cv2.imread(self.path + 'imR.png')

        imgLeftGray = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
        imgRightGray = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)
        disparity = stereo.compute(imgLeftGray, imgRightGray) / 16
        disparity = self.setImageSize(disparity)
        disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        self.imgLeft = self.setImageSize(imgLeft)
        self.imgRight = self.setImageSize(imgRight)
        self.disparity = self.setDisparitySale(disparity)
        self.showDisparity = disparity

        self.isCal = True


    def stereo_disparity_map(self):
        if self.isCal == False:
            self.disparity_calculate()

        cv2.imshow('disparity', self.showDisparity)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    def mouseEventHanlder(self, event, x, y, flags, params):
        if event == 1:
            imgLeft = copy.deepcopy(self.imgLeft)
            imgRight = copy.deepcopy(self.imgRight)

            cv2.line(imgLeft, (x, y), (x, y), (0, 0, 255), 10)
            cv2.imshow('imgLeft', imgLeft)

            cv2.line(imgRight, (x - self.disparity[y][x], y), (x - self.disparity[y][x], y), (0, 255, 0), 10)
            cv2.imshow('imgRight', imgRight)


    def check_disparity_value(self):
        if self.isCal == False:
            self.disparity_calculate()

        cv2.imshow('imgLeft', self.imgLeft)
        cv2.imshow('imgRight', self.imgRight)

        cv2.setMouseCallback("imgLeft", self.mouseEventHanlder)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
