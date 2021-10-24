import cv2
import numpy as np
from glob import glob
import copy

class corner_detection():

    def __init__(self, path):
        self.isCal = False
        self.images = []
        self.path = path


    def setPath(self, path):
        self.path = path


    def find_corners(self, visiable):
        nx = 11
        ny = 8

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0), ...(6,5,0)
        objp = np.zeros((nx*ny,3), np.float32)
        objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d points in real world space
        imgpoints = [] # 2d pionts in image plane.
        images = []
        
        paths = glob(self.path + '*.bmp')
        for idx, fname in enumerate(paths):
            img = cv2.imread(fname)
            images.append(copy.deepcopy(img))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)

            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

                if visiable:
                    cv2.drawChessboardCorners(img, (nx,ny), corners, ret)
                    shape = np.shape(img)
                    image = cv2.resize(img, (shape[1] // 3, shape[0] // 3), interpolation=cv2.INTER_AREA)
                    # write_name = 'corners_found'+str(idx + 1)+'.jpg'
                    # cv2.imwrite(self.path + write_name, image)
                    cv2.imshow('img', image)
                    cv2.waitKey(500)

        cv2.destroyAllWindows()

        _, self.intrinsic, self.distortion, self.rotations, self.translations = cv2.calibrateCamera(objpoints, imgpoints, (img.shape[1],img.shape[0]), None, None)
        self.images = images
        self.isCal = True    


    def find_intrinsic(self):
        if self.isCal == False:
            self.find_corners(False)

        print("intrinsic matrix = ")
        print(self.intrinsic)


    def find_extrinsic(self, index):
        if self.isCal == False:
            self.find_corners(False)

        rotation, _ = cv2.Rodrigues(self.rotations[index])
        translation = self.translations[index]
        extrinsic = np.concatenate((rotation, translation), axis = 1)

        print("extrinsic matrix = ")
        print(extrinsic)


    def find_distortion(self):
        if self.isCal == False:
            self.find_corners(False)

        print("distortion matrix = ")
        print(self.distortion)


    def show(self):
        if self.isCal == False:
            self.find_corners(False)

        for idx, image in enumerate(self.images):
            h, w = image.shape[:2]
            newCameraMatrix, (x, y, w, h) = cv2.getOptimalNewCameraMatrix(self.intrinsic, self.distortion, (h, w), 1, (h, w))
            undistortImage = cv2.undistort(image, self.intrinsic, self.distortion, None, newCameraMatrix)
            
            showResult = np.concatenate((image, undistortImage), axis=1)
            shape = np.shape(showResult)
            showResult = cv2.resize(showResult, (shape[1] // 3, shape[0] // 3), interpolation=cv2.INTER_AREA)
            
            # cv2.imwrite(self.path + 'undistortImage{}.png'.format(idx + 1), undistortImage)
            cv2.imshow('distortImage & undistortImage', showResult)
            cv2.waitKey(500)

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


