from Data_Processing import data_processing
from Data_Analyze import data_analyze
from glob import glob
import matplotlib.pylab as plt
from scipy.stats import wasserstein_distance
import numpy as np
import cv2
from scipy.fft import fft2


class detect_shot_change(data_processing):

    def __init__(self, args):
        self.data_analyze = data_analyze()

        self.threshold = args.threshold
        self.windowSize = args.windowSize

        self.loss = []
        self.result = []

        self.load_image(args.imagePath)
        self.readGroundTruth(args.groundTruthFile)


    ###################### Algorithm 1 => color_histogram ######################

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
        total = 256 // self.windowSize

        for i in range(len(self.images) - 1):
            gray1 = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
            hist1 = cv2.calcHist([gray1], [0], None, [total], [0, 256])

            gray2 = cv2.cvtColor(self.images[i + 1], cv2.COLOR_BGR2GRAY)
            hist2 = cv2.calcHist([gray2], [0], None, [total], [0, 256])

            self.loss.append(np.mean(abs(hist1 - hist2)))
            # self.loss.append(self.compare_histogram(hist1, hist2, total))

        plt.plot(self.loss)
        plt.show()


    def getColorShotChangeFrame(self):
        if self.loss == []:
            self.color_histogram()

        self.result = []
        for i in range(len(self.loss) - 1):
            if self.loss[i] > self.threshold:
                self.result.append(i + 1)

        self.result = self.data_analyze.dataAdjust(self.result)
        
        # print(self.result)
        precision, recall = self.data_analyze.getAccuracy(self.result, self.groundTruth)
        print("precision = {}, recall = {}".format(precision, recall))


    ###################### Algorithm 2 => keyPoints_dection ######################

    def keyPoints_dection(self):

        self.loss = []
        origin_loss = []

        for i in range(len(self.images) - 1):
            image1 = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
            image2 = cv2.cvtColor(self.images[i + 1], cv2.COLOR_BGR2GRAY)

            ########################## find keypoint ##########################

            sift = cv2.xfeatures2d.SIFT_create()

            keypoint1, des1 = sift.detectAndCompute(image1, None)
            keypoint2, des2 = sift.detectAndCompute(image2, None)

            # if keypoint1 == [] or keypoint2 == []:
            #     self.loss.append(0)
            #     continue

            try:
                keypoint1, des1 = zip(*sorted(zip(keypoint1, des1), key = lambda x: x[0].size, reverse = True)[:200])
                keypoint2, des2 = zip(*sorted(zip(keypoint2, des2), key = lambda x: x[0].size, reverse = True)[:200])

                keypoint1, des1 = np.array(keypoint1), np.array(des1)
                keypoint2, des2 = np.array(keypoint2), np.array(des2)

                ########################## find keypoint ##########################

                flann = cv2.FlannBasedMatcher(dict(algorithm = 1, trees = 5), dict(checks = 50))

                matches = flann.knnMatch(des1, des2, k = 2)
                # goodMatch = [m for m, n in matches if m.distance < 0.7 * n.distance]

                distance = [m.distance for m, n in matches]
                total_distance = np.mean(distance)

                # print(len(matches))
                # origin_loss.append(len(matches))

                print(total_distance)
                origin_loss.append(total_distance)

            except:
                print(0)
                origin_loss.append(0)

        k = 5
        self.loss = []
        for i in range(len(origin_loss)):
            self.loss.append(np.median(origin_loss[max(0, i - k // 2): i + k // 2]))

        plt.plot(self.loss)
        plt.savefig("./dataset/Result/current.png")
        plt.show()


    def getKeypointShotChangeFrame(self):
        if self.loss == []:
            self.keyPoints_dection()

        k = 5
        self.result = []
        for i in range(len(self.loss)):
            hit = True
            candidate = self.loss[i]
            for loss in self.loss[max(i - k // 2, 0): i + k // 2]:
                if candidate > loss:
                    hit = False
                    break
            
            if hit:
                self.result.append(i + 1)

        self.result = self.data_analyze.dataAdjust(self.result)
        
        print(self.result)
        precision, recall = self.data_analyze.getAccuracy(self.result, self.groundTruth, 3)
        print("precision = {}, recall = {}".format(precision, recall))


    ###################### Algorithm 3 => fourier_transform ######################

    def fourier_transform(self):

        self.loss = []
        origin_loss = []

        for i in range(len(self.images) - 1):
            image1 = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
            image2 = cv2.cvtColor(self.images[i + 1], cv2.COLOR_BGR2GRAY)

            imageFourier1 = np.abs(fft2(image1))
            imageFourier2 = np.abs(fft2(image2))

            lossVal = np.mean(np.abs(imageFourier1 - imageFourier2))
            print(lossVal)
            origin_loss.append(lossVal)

        k = 5
        self.loss = []
        for i in range(len(origin_loss)):
            self.loss.append(np.median(origin_loss[max(0, i - k // 2): i + k // 2]))

        plt.plot(self.loss)
        plt.show()


    def getFourierShotChangeFrame(self):
        if self.loss == []:
            self.fourier_transform()

        k = 5
        self.result = []
        for i in range(len(self.loss)):
            hit = True
            candidate = self.loss[i]
            for loss in self.loss[max(i - k // 2, 0): i + k // 2]:
                if candidate < loss:
                    hit = False
                    break
            
            if hit:
                self.result.append(i + 1)

        self.result = self.data_analyze.dataAdjust(self.result)
        
        print(self.result)
        precision, recall = self.data_analyze.getAccuracy(self.result, self.groundTruth, 3)
        print("precision = {}, recall = {}".format(precision, recall))