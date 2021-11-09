import numpy as np
import cv2


class transforms():

    def __init__(self, path):
        self.setPath(path)


    def setPath(self, path):
        self.path = path
        self.SQUARE_image = cv2.imread(self.path + "SQUARE-01.png")


    def resize(self):
        self.resizeImage = cv2.resize(self.SQUARE_image, (256, 256), interpolation=cv2.INTER_AREA)

        cv2.imshow("Resize", self.resizeImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def translation(self):
        M = np.float32([
            [1, 0,  0],
            [0, 1, 60]
        ])
        self.translateImage = cv2.warpAffine(self.resizeImage, M, (400, 300))

        cv2.imshow("translation", self.translateImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def scaling_rotation(self):
        M = np.float32([
            [0.5, 0.0, 0.0],
            [0.0, 0.5, 0.0]
        ])
        self.scaleImage = cv2.warpAffine(self.resizeImage, M, (400, 300))

        M = np.float32([
            [1, 0, 128],
            [0, 1, 188]
        ])
        self.scaleImage = cv2.warpAffine(self.scaleImage, M, (400, 300))

        theta = 10 * np.pi / 180
        M = np.float32([
            [ np.cos(theta),  np.sin(theta), 0.0],
            [-np.sin(theta),  np.cos(theta), 0.0]
        ])
        self.scaleImage = cv2.warpAffine(self.scaleImage, M, (400, 300))

        # cv2.getRotationMatrix2D(()) ??

        cv2.imshow("translation", self.scaleImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def shearing(self):
        pass
        # M = np.float32([
        #     [1, 0, 128],
        #     [0, 1, 188]
        # ])
        # source = np.array([[50,50],[200,50],[50,200]], dtype="uint8")
        # destination = np.array([[10,100],[200,50],[100,250]], dtype="uint8")
        # M = cv2.getAffineTransform(source, destination)
        # print(M)

