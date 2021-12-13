from matplotlib.pyplot import imshow
from sklearn.decomposition import PCA
import matplotlib.pylab as plt
import numpy as np
import cv2

class pca():

    def __init__(self, path):
        self.path = path
        self.origin_images = []
        self.transfer_images = []


    def setPath(self, path):
        self.path = path

    
    def readImage(self):
        for i in range(1, 30 + 1):
            image = cv2.imread(self.path + "{}.jpg".format(i))
            self.origin_images.append(image)


    def pca_transform(self, image):
        pca_method = PCA(20)
        transformed = pca_method.fit_transform(image)
        inverted = pca_method.inverse_transform(transformed)
        return cv2.normalize(inverted, inverted, 0, 255, cv2.NORM_MINMAX)


    def image_reconstruction(self, visiable = True):
        if self.origin_images == []:
            self.readImage()
        
        for i in range(30):
            blue, green, red = cv2.split(self.origin_images[i]) 
            transfer_image = (np.dstack((self.pca_transform(blue), self.pca_transform(green), self.pca_transform(red)))).astype(np.uint8)
            self.transfer_images.append(transfer_image)

        if visiable:
            self.showImage()

    def compute_reconstruction_error(self):
        if self.transfer_images == []:
            self.image_reconstruction()

        error = []
        for i in range(30):
            origin_image, transfer_image = cv2.cvtColor(self.origin_images[i], cv2.COLOR_BGR2GRAY), cv2.cvtColor(self.transfer_images[i], cv2.COLOR_BGR2GRAY)
            error.append(np.sum(np.abs(transfer_image - origin_image)))

        print(error)

    
    def showImage(self):
        if self.transfer_images == []:
            self.image_reconstruction()

        size = 16

        plt.subplot(4, 15, 1)
        plt.ylabel("origin", fontsize = size)

        plt.subplot(4, 15, 16)
        plt.ylabel("reconstruction", fontsize = size)

        plt.subplot(4, 15, 31)
        plt.ylabel("origin", fontsize = size)

        plt.subplot(4, 15, 46)
        plt.ylabel("reconstruction", fontsize = size)

        for i in range(15):

            plt.subplot(4, 15, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.origin_images[i])

            plt.subplot(4, 15, i + 16)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.transfer_images[i])

        for i in range(15, 30):

            plt.subplot(4, 15, i + 16)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.origin_images[i])

            plt.subplot(4, 15, i + 31)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.transfer_images[i])

        plt.get_current_fig_manager().window.showMaximized()
        plt.show()
