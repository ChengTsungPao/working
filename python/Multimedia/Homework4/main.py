"""
Segmentation with Gaussian mixture models
=========================================

This example performs a Gaussian mixture model analysis of the image
histogram to find the right thresholds for separating foreground from
background.

"""

import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import cv2

path = "./dataset/hw4/"
filename = "soccer1.jpg"

np.random.seed(1)
image = cv2.imread(path + filename, 0)
# l = image.shape[0]
# n = 10
# image = ndimage.gaussian_filter(image, sigma=l/(4.*n))


hist, bin_edges = np.histogram(image, bins=60)
bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

classif = GaussianMixture(n_components=10)
classif.fit(image)

threshold = np.mean(classif.means_)
binary_image = image < threshold


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
