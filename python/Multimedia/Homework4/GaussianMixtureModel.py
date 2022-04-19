import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import collections
import cv2
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


##################################### create gaussian mixture model #####################################

class gaussianMixtureModel:

    def __init__(self, path = "./"):
        self.path = path
        self.resetGaussianMixtureModel()


    def resetGaussianMixtureModel(self):
        self.GMM_Model = []
        self.predictImage = []
        self.histogram = []
        self.binaryImage = []


    def getGaussianMixtureModel(self, filenames, n = 2):
        print("\nCreate Gaussian Mixture Model by {} (n_components = {})".format(filenames, n))
        np.random.seed(1)

        images = []
        for filename in filenames:
            image = cv2.imread(self.path + filename)
            images += list(image.reshape((-1, 3)))
        imageReshape = np.array(images)

        self.GMM_Model = GaussianMixture(n_components = n).fit(imageReshape)

        
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
        return self.calculateAccuracy(filename)


    def calculateAccuracy(self, filename):
        count = collections.defaultdict(int)
        for x, y, label in pd.read_csv(self.path + '{}_mask.csv'.format(filename.split(".")[0])).values.tolist():
            predict = self.binaryImage[x][y]
            count[predict, label] += 1
        TP, FP, TN, FN = count[1, 1], count[1, 0], count[0, 0], count[0, 1]   
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        print("    {}: precision = {}, recall = {}".format(filename, precision, recall))
        return precision, recall

    
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


########################### test difference n_components in gaussian mixture model ##############################

def test_gaussianMixtureModel(path, soccer1_filename, soccer2_filename, n_components_range = [2, 10]):
    gmm_func = gaussianMixtureModel(path)

    n_components = list(range(n_components_range[0], n_components_range[1]))
    soccer1_precisions = []
    soccer2_precisions = []
    soccer1_recalls = []
    soccer2_recalls = []

    for n in n_components:
        gmm_func.getGaussianMixtureModel([soccer1_filename, soccer2_filename], n)
        
        soccer1_precision, soccer1_recall = gmm_func.predictGaussianMixtureModel(soccer1_filename, n == 5)
        soccer2_precision, soccer2_recall = gmm_func.predictGaussianMixtureModel(soccer2_filename)
        soccer1_precisions.append(soccer1_precision)
        soccer2_precisions.append(soccer2_precision)
        soccer1_recalls.append(soccer1_recall)
        soccer2_recalls.append(soccer2_recall)

    plt.clf()
    plt.title(soccer1_filename)
    plt.plot(n_components, soccer1_precisions, "-o", label = "precision")
    plt.plot(n_components, soccer1_recalls, "-o", label = "recall")
    plt.xlabel("n_components")
    plt.ylabel("accuracy")
    plt.legend()
    plt.show()

    plt.clf()
    plt.title(soccer2_filename)
    plt.plot(n_components, soccer2_precisions, "-o", label = "precision")
    plt.plot(n_components, soccer2_recalls, "-o", label = "recall")
    plt.xlabel("n_components")
    plt.ylabel("accuracy")
    plt.legend()
    plt.show()