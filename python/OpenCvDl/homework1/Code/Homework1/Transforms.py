import numpy as np
import cv2


class transforms():

    def __init__(self, path):
        self.setPath(path)


    def setPath(self, path):
        self.path = path
        self.SQUARE_image = cv2.imread(self.path + "SQUARE-01.png")
        self.resizeImage = []
        self.translateImage = []
        self.scaleRotationImage = []


    def resize(self, visible = True):
        self.resizeImage = cv2.resize(self.SQUARE_image, (256, 256), interpolation=cv2.INTER_AREA)

        if visible:
            self.showImage("Resize", self.resizeImage)


    def translation(self, visible = True):
        if self.resizeImage == []:
            self.resize(False)

        M = np.float32([
            [1, 0,  0],
            [0, 1, 60]
        ])
        self.translateImage = cv2.warpAffine(self.resizeImage, M, (400, 300))

        if visible:
            self.showImage("translation", self.translateImage)


    def scaling_rotation(self, visible = True):
        if self.translateImage == []:
            self.translation(False)

        M = cv2.getRotationMatrix2D((128, 188), 10, 0.5)
        self.scaleRotationImage = cv2.warpAffine(self.translateImage, M, (400, 300))

        if visible:
            self.showImage("scaling & rotation", self.scaleRotationImage)


    def shearing(self, visible = True):
        if self.scaleRotationImage == []:
            self.scaling_rotation(False)

        source = np.float32([[50,50], [200,50], [50,200]])
        destination = np.float32([[10,100], [200,50], [100,250]])
        M = cv2.getAffineTransform(source, destination)
        self.shearImage = cv2.warpAffine(self.scaleRotationImage, M, (400, 300))
        
        if visible:
            self.showImage("shearing", self.shearImage)


    def showImage(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

