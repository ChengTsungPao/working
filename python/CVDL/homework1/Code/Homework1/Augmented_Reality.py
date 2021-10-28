from Corner_Detection import corner_detection
from glob import glob
import numpy as np
import cv2

class augmented_reality(corner_detection):
    def __init__(self, path):
        super().__init__(path)
        self.find_intrinsic(False)


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

            cv2.imshow('augmented_reality_image', self.setImageSize(image))
            cv2.waitKey(500)

        cv2.destroyAllWindows()


    def draw_board(self, word):
        if word != "" and word.isalpha() == False:
            return

        fs = cv2.FileStorage(self.path + "Q2_lib//" + "alphabet_lib_onboard.txt", cv2.FILE_STORAGE_READ)
        self.draw(word.upper(), fs)
        

    def draw_vertical(self, word):
        if word != "" and word.isalpha() == False:
            return

        fs = cv2.FileStorage(self.path + "Q2_lib//" + "alphabet_lib_vertical.txt", cv2.FILE_STORAGE_READ)                
        self.draw(word.upper(), fs)
