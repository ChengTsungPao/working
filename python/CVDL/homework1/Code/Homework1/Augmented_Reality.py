from Corner_Detection import corner_detection
from glob import glob
import numpy as np
import cv2

class augmented_reality(corner_detection):
    def __init__(self, path):
        super().__init__(path)
        self.find_intrinsic(False)


    def perspective_transfer(self, point3D):

        point3D = np.array([[point3D[0]], [point3D[1]], [point3D[2]], [1]])
        point2D = np.dot(self.cameraMatrix, point3D)
        point2D = point2D[:2] / point2D[2]

        return (int(point2D[0][0]), int(point2D[1][0]))


    def distortion_transfer(self, point2D):

        x, y = point2D[0], point2D[1]
        r = x ** 2 + y ** 2
        k1, k2, p1, p2, k3 = self.distortion[0][0], self.distortion[0][1], self.distortion[0][2], self.distortion[0][3], self.distortion[0][4]

        x = x * (1 + k1 * r ** 2 + k2 * r ** 4 + k3 * r ** 6)
        y = y * (1 + k1 * r ** 2 + k2 * r ** 4 + k3 * r ** 6)

        x = x + (2 * p1 * x * y + p2 * (r ** 2 + 2 * x ** 2))
        y = y + p1 * (r ** 2 + 2 * y ** 2) + 2 * p2 * x * y

        return int(x), int(y)


    def character_shift(self, position, chIndex):

        if chIndex == 1 or chIndex == 2 or chIndex == 3:
            position[1] += 5
        else:
            position[1] += 2

        if chIndex == 1 or chIndex == 4:
            position[0] += 7
        elif chIndex == 2 or chIndex == 5:
            position[0] += 4
        else:
            position[0] += 1

        return position


    def drawSelf(self, word, fs):
        paths = glob(self.path + '*.bmp')  

        for pathIndex, path in enumerate(paths):
            distortImage = cv2.imread(path)

            h, w = distortImage.shape[:2]
            newCameraMatrix, _ = cv2.getOptimalNewCameraMatrix(self.intrinsic, self.distortion, (h, w), 1, (h, w))
            undistortImage = cv2.undistort(distortImage, self.intrinsic, self.distortion, None, newCameraMatrix)

            self.find_extrinsic(pathIndex, False)
            self.cameraMatrix = np.dot(self.intrinsic, self.extrinsic)   

            for chIndex, ch in enumerate(word):
                lines = fs.getNode(ch).mat() 

                for line in lines:
                    start, end = line
                    start, end = self.character_shift(start, chIndex + 1), self.character_shift(end, chIndex + 1)
                    cv2.line(distortImage, self.distortion_transfer(self.perspective_transfer(start)), self.distortion_transfer(self.perspective_transfer(end)), (0, 0, 255), 20)

            cv2.imshow('image', self.setImageSize(distortImage))
            cv2.waitKey(500)

        cv2.destroyAllWindows()


    def draw(self, word, fs):
        paths = glob(self.path + '*.bmp')  

        for pathIndex, path in enumerate(paths):
            image = cv2.imread(path)
    
            for chIndex, ch in enumerate(word):
                lines = fs.getNode(ch).mat() 

                for line in lines:
                    lineShift = [self.character_shift(pos, chIndex + 1) for pos in line]
                    points, _ = cv2.projectPoints(np.float32(lineShift), self.rotations[pathIndex], self.translations[pathIndex], self.intrinsic, self.distortion)
                    points = np.int32(points).reshape(-1, 2)
                    start, end = tuple(points[0]), tuple(points[1])
                    cv2.line(image, start, end, (0, 0, 255), 10)

            cv2.imshow('image', self.setImageSize(image))
            cv2.waitKey(500)

        cv2.destroyAllWindows()


    def draw_board(self, word):
        fs = cv2.FileStorage(self.path + "Q2_lib//" + "alphabet_lib_onboard.txt", cv2.FILE_STORAGE_READ)
        self.draw(word, fs)
        

    def draw_vertical(self, word):
        fs = cv2.FileStorage(self.path + "Q2_lib//" + "alphabet_lib_vertical.txt", cv2.FILE_STORAGE_READ)                
        self.draw(word, fs)
