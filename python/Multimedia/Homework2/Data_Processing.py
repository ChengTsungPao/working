import cv2
from Function import Union_Find
from glob import glob

class data_processing():

    def __init__(self):
        self.images = []
        self.groundTruth = Union_Find()


    def readGroundTruth(self, groundTruthFile):
        f = open(groundTruthFile, "r")
        lines = f.readlines()[4:]
        self.groundTruth = Union_Find()

        for line in lines:
            line = line.split("\n")[0]
            line = line.strip()

            if "~" in line:
                start, end = line.split("~")
                start, end = int(start), int(end)
            else:
                start = int(line)
                end = start

            self.groundTruth.build(start)
            for i in range(start + 1, end):
                self.groundTruth.build(i)
                self.groundTruth.union(start, i)


    def load_image(self, folderPath):
        self.images = []
        imagePaths = glob(folderPath + "*")
        for imagePath in imagePaths:
            self.images.append(cv2.imread(imagePath))