from glob import glob
import matplotlib.pylab as plt
from scipy.stats import wasserstein_distance
import numpy as np
import cv2


class shot_change_detection():

    def __init__(self, imagePath, groundTruthFile):
        self.images = []
        self.groundTruth = []
        self.load_image(imagePath)
        self.readGroundTruth(groundTruthFile)


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
        ans = []
        loss = []
        total = 256 // 8

        for i in range(len(self.images) - 1):
            gray1 = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
            hist1 = cv2.calcHist([gray1], [0], None, [total], [0, 256])

            gray2 = cv2.cvtColor(self.images[i + 1], cv2.COLOR_BGR2GRAY)
            hist2 = cv2.calcHist([gray2], [0], None, [total], [0, 256])

            loss.append(np.mean(abs(hist1 - hist2)))
            # loss.append(self.compare_histogram(hist1, hist2, total))

            # if loss[-1] > 750:
            # if loss[-1] > 1340:
            #     ans.append(i + 1)

        print(ans)
        plt.plot(loss)
        plt.plot(self.groundTruth, [10] * len(self.groundTruth), "o")
        plt.show()
