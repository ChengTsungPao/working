from glob import glob
import matplotlib.pylab as plt
from scipy.stats import wasserstein_distance
import numpy as np
import cv2


class shot_change_detection():

    def __init__(self, args):
        # self.windowSize = args.windowSize

        self.loss = []
        self.result = []

        self.images = []
        self.groundTruth = []
        self.load_image(args.imagePath)
        self.readGroundTruth(args.groundTruthFile)


    def readGroundTruth(self, groundTruthFile):
        f = open(groundTruthFile, "r")
        lines = f.readlines()[4:]
        self.groundTruth = []
        for line in lines:
            line = line.split("\n")[0]
            line = line.strip()
            if "~" in line:
                start, end = line.split("~")
                start, end = int(start), int(end)
            else:
                start = int(line)
            self.groundTruth.append(start)


    def load_image(self, folderPath):
        self.images = []
        imagePaths = glob(folderPath + "*")
        for imagePath in imagePaths:
            self.images.append(cv2.imread(imagePath))


    def compare_histogram(self, hist1, hist2, total):

        sigma = 0.5
        def G(x):
            times = - (x ** 2) / (2 * sigma ** 2)
            return (np.e ** times) / (2 * np.pi * sigma ** 2)

        unit = 6 * sigma / total
        difference = []
        for i in range(len(hist1)):
            s = 0
            w = 0
            for j in range(len(hist2)):
                s += abs(hist2[j] - hist1[i]) * G((j - i) * unit)
                w += G((j - i) * unit)
            difference.append(s / w)

        return np.mean(difference)


    def color_histogram(self):
        self.loss = []
        total = 256 // 8

        for i in range(len(self.images) - 1):
            gray1 = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
            hist1 = cv2.calcHist([gray1], [0], None, [total], [0, 256])

            gray2 = cv2.cvtColor(self.images[i + 1], cv2.COLOR_BGR2GRAY)
            hist2 = cv2.calcHist([gray2], [0], None, [total], [0, 256])

            self.loss.append(np.mean(abs(hist1 - hist2)))
            # self.loss.append(self.compare_histogram(hist1, hist2, total))

        plt.plot(self.loss)
        plt.plot(self.groundTruth, [10] * len(self.groundTruth), "o")
        plt.show()

    
    def getShotChangeFrame(self):
        if self.loss == []:
            self.color_histogram()

        self.result = []
        for i in range(len(self.loss) - 1):
            if self.loss[i] > 750:
            # if self.loss[-1] > 1340:
                self.result.append(i + 1)

        print(self.result)
