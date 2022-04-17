import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import collections
import cv2
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


class gaussianMixtureModel:

    def __init__(self, path = "./"):
        self.path = path
        self.GMM_Model = []
        self.predictImage = []
        self.histogram = []
        self.binaryImage = []


    def getGaussianMixtureModel(self, filenames):
        print("\nCreate Gaussian Mixture Model by {}".format(filenames))
        np.random.seed(1)

        images = []
        for filename in filenames:
            image = cv2.imread(self.path + filename)
            images += list(image.reshape((-1, 3)))
        imageReshape = np.array(images)

        self.GMM_Model = GaussianMixture(n_components=2).fit(imageReshape)

        
    def predictGaussianMixtureModel(self, filename, reverse = False):
        if self.GMM_Model == []:
            return

        np.random.seed(1)
        self.predictImage = cv2.imread(self.path + filename)
        imageReshape = self.predictImage.reshape((-1, 3))

        self.histogram = np.histogram(self.predictImage, bins=100)

        gmm_label = self.GMM_Model.predict(imageReshape)
        self.binaryImage = gmm_label.reshape((self.predictImage.shape[0], self.predictImage.shape[1]))
        self.binaryImage = np.where(self.binaryImage, (not reverse) * 1, reverse * 1)

        self.calculateAccuracy(filename)


    def calculateAccuracy(self, filename):
        count = collections.defaultdict(int)
        for x, y, label in pd.read_csv(self.path + '{}_mask.csv'.format(filename.split(".")[0])).values.tolist():
            predict = self.binaryImage[x][y]
            count[predict, label] += 1
        TP, FP, TN, FN = count[1, 1], count[1, 0], count[0, 0], count[0, 1]   
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        print("    {}: precision = {}, recall = {}".format(filename, precision, recall))

    
    def plotResult(self):
        if self.binaryImage == []:
            return

        hist, bin_edges = self.histogram
        bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

        plt.figure(figsize=(11,4))
        plt.subplot(131)
        plt.axis('off')
        plt.imshow(self.predictImage)

        plt.subplot(132)
        plt.yticks([])
        plt.plot(bin_centers, hist, lw=2)

        plt.subplot(133)
        plt.axis('off')
        plt.imshow(self.binaryImage, cmap=plt.cm.gray, interpolation='nearest')

        plt.subplots_adjust(wspace=0.02, hspace=0.3, top=1, bottom=0.1, left=0, right=1)
        plt.show()