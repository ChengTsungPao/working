import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import cv2
import pandas as pd

def GaussianMixtureModel(path, filename):

    np.random.seed(1)
    image = cv2.imread(path + filename)
    imageReshape = image.reshape((-1, 3))

    hist, bin_edges = np.histogram(image, bins=60)
    bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

    GMM_Model = GaussianMixture(n_components=2).fit(imageReshape)
    gmm_label = GMM_Model.predict(imageReshape)
    binary_image = gmm_label.reshape((image.shape[0], image.shape[1]))
    binary_image = np.where(binary_image, 0, 1)

    plt.figure(figsize=(11,4))
    plt.subplot(131)
    plt.axis('off')
    plt.imshow(image)

    plt.subplot(132)
    plt.yticks([])
    plt.plot(bin_centers, hist, lw=2)

    plt.subplot(133)
    plt.axis('off')
    plt.imshow(binary_image, cmap=plt.cm.gray, interpolation='nearest')

    plt.subplots_adjust(wspace=0.02, hspace=0.3, top=1, bottom=0.1, left=0, right=1)
    plt.show()

if __name__ == "__main__":

    path = "./dataset/hw4/"
    filename = "soccer1.jpg"
    GaussianMixtureModel(path, filename)

    soccer1_groundTruth = {}
    for x, y, label in pd.read_csv(path + 'soccer1_mask.csv').values.tolist():
        soccer1_groundTruth[x, y] = label

