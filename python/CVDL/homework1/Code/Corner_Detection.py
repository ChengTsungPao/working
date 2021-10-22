import cv2
import numpy as np
from glob import glob

class corner_detection():

    def find_corners(self, path, visiable):
        '''
        read the calibration image and do the camera calibration
        and output the result to a pickle file.
        if drawconer is True, will draw the corner on the chessboard file and save it to another folder.
        '''
        # !!! IMPORTANT, set the nx, ny according the calibration chessboard pictures.
        nx = 11
        ny = 8

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0), ...(6,5,0)
        objp = np.zeros((nx*ny,3), np.float32)
        objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d points in real world space
        imgpoints = [] # 2d pionts in image plane.

        # Make a list of calibration images
        
        images = glob(path + '*.bmp')
        # print("Reading the calibration file...")

        # Step through the list and search for chessboard corners
        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            # print("Searching corners on ", fname, "...")
            ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)

            # If found, add object points, image points
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

                if visiable:

                    cv2.drawChessboardCorners(img, (nx,ny), corners, ret)

                    shape = np.shape(img)
                    image = cv2.resize(img, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)

                    write_name = 'corners_found'+str(idx + 1)+'.jpg'
                    cv2.imwrite(path + write_name, image)
                    cv2.imshow('img', image)
                    cv2.waitKey(500)

        cv2.destroyAllWindows()

        # Get image size
        img_size = (img.shape[1],img.shape[0])

        # Do camera calibration given object points and image points
        _, self.intrinsic, self.distortation, self.rotations, self.translations = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    

    def find_intrinsic(self):
        print("intrinsic matrix = ")
        print(self.intrinsic)

    def find_extrinsic(self, index):
        rotation, _ = cv2.Rodrigues(self.rotations[index])
        translation = self.translations[index]
        extrinsic = np.concatenate((rotation, translation), axis = 1)

        print("extrinsic matrix = ")
        print(extrinsic)

    def show(self):
        pass


