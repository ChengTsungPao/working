import cv2
import numpy as np
from glob import glob
import copy

class corner_detection():

    def __init__(self, path):
        self.images = []
        self.intrinsic = None
        self.extrinsic = None
        self.distortion = None
        self.rotations = None
        self.translations = None
        self.path = path

        self.scale = 3
        self.isCal = False


    def setPath(self, path):
        self.path = path

    def setImageSize(self, image):
        shape = np.shape(image)
        return cv2.resize(image, (shape[1] // self.scale, shape[0] // self.scale), interpolation=cv2.INTER_AREA)

    def find_corners(self, visiable = True):
        nx = 11
        ny = 8

        images = []
        point3D = []
        point2D = []
        
        points = np.zeros((nx * ny, 3), np.float32)
        points[ :, : 2] = np.mgrid[0 : nx, 0 : ny].T.reshape(-1,2)

        paths = glob(self.path + '*.bmp')
        for index, fname in enumerate(paths):
            image = cv2.imread(fname)
            images.append(copy.deepcopy(image))

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

            if ret == True:
                point3D.append(points)
                point2D.append(corners)

                if visiable:
                    cv2.drawChessboardCorners(image, (nx, ny), corners, ret)
                    showImage = self.setImageSize(image)
                    # cv2.imwrite(self.path + "corners_found{}.jpg".format(index + 1), showImage)
                    cv2.imshow("corners_found", showImage)
                    cv2.waitKey(500)

        cv2.destroyAllWindows()

        ret = cv2.calibrateCamera(point3D, point2D, (image.shape[1],image.shape[0]), None, None)
        
        self.intrinsic = ret[1]
        self.distortion = ret[2]
        self.rotations = ret[3]
        self.translations = ret[4]
        self.images = images
        self.isCal = True    


    def find_intrinsic(self, visiable = True):
        if self.isCal == False:
            self.find_corners(False)

        if visiable:
            print("intrinsic matrix = ")
            print(self.intrinsic)


    def find_extrinsic(self, index, visiable = True):
        if index == "":
            index = "1"

        if index.isdigit() == False:
            return

        if self.isCal == False:
            self.find_corners(False)

        index = int(index) - 1
        if not 0 <= index < len(self.translations):
            return

        rotation, _ = cv2.Rodrigues(self.rotations[index])
        translation = self.translations[index]
        self.extrinsic = np.concatenate((rotation, translation), axis = 1)

        if visiable:
            print("extrinsic matrix = ")
            print(self.extrinsic)


    def find_distortion(self):
        if self.isCal == False:
            self.find_corners(False)

        print("distortion matrix = ")
        print(self.distortion)


    def show(self):
        if self.isCal == False:
            self.find_corners(False)

        for index, image in enumerate(self.images):
            h, w = image.shape[:2]
            newCameraMatrix, (x, y, w, h) = cv2.getOptimalNewCameraMatrix(self.intrinsic, self.distortion, (h, w), 1, (h, w))
            undistortImage = cv2.undistort(image, self.intrinsic, self.distortion, None, newCameraMatrix)
            
            showResult = np.concatenate((image, undistortImage), axis=1)
            showResult = self.setImageSize(showResult)
            
            # cv2.imwrite(self.path + "undistortImage{}.png".format(index + 1), undistortImage)
            cv2.imshow("distortImage & undistortImage", showResult)
            cv2.waitKey(500)

        cv2.destroyAllWindows()


