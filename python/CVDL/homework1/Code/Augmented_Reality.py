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
        return (point2D[0][0], point2D[1][0])


    def draw(self, word, fs):
        paths = glob(self.path + '*.bmp')  

        for index, path in enumerate(paths):
            image = cv2.imread(path)
            self.find_extrinsic(index, False)
            self.cameraMatrix = np.dot(self.intrinsic, self.extrinsic)   

            for ch in word:
                lines = fs.getNode(ch).mat() 

                for line in lines:
                    start, end = line
                    print(self.perspective_transfer(start))
                    print(self.perspective_transfer(end))
                    # cv2.line(image, self.perspective_transfer(start), self.perspective_transfer(end), (0, 0, 255), 5)

            cv2.imshow('image', self.setImageSize(image))
            cv2.waitKey(500)

        cv2.destroyAllWindows()


    def draw_board(self, word):
        fs = cv2.FileStorage(self.path + "Q2_lib//" + "alphabet_lib_onboard.txt", cv2.FILE_STORAGE_READ)
        self.draw(word, fs)
        
        
    def draw_vertical(self, word):
        fs = cv2.FileStorage(self.path + "Q2_lib//" + "alphabet_lib_vertical.txt", cv2.FILE_STORAGE_READ)                
        self.draw(word, fs)
