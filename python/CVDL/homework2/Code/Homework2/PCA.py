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
            blue, green, red = cv2.split(image)
            image = cv2.merge([red, green, blue])
            self.origin_images.append(image)


    def pca_transform(self, image):
        pca_method = PCA(20)
        transformed = pca_method.fit_transform(image)
        inverted = pca_method.inverse_transform(transformed)
        return inverted


    def image_reconstruction(self, visiable = True):
        if self.origin_images == []:
            self.readImage()
        
        for i in range(30):
            red, green, blue = cv2.split(self.origin_images[i]) 
            transfer_image = (np.dstack((self.pca_transform(red), self.pca_transform(green), self.pca_transform(blue))))
            self.transfer_images.append(transfer_image)

        if visiable:
            self.showImage()


    def compute_reconstruction_error(self):
        if self.transfer_images == []:
            self.image_reconstruction(False)

        error = []
        for i in range(30):
            origin_image, transfer_image = cv2.normalize(self.origin_images[i].astype(np.uint8), None, 0, 255, cv2.NORM_MINMAX), cv2.normalize(self.transfer_images[i].astype(np.uint8), None, 0, 255, cv2.NORM_MINMAX)
            origin_image, transfer_image = cv2.cvtColor(origin_image, cv2.COLOR_BGR2GRAY), cv2.cvtColor(transfer_image, cv2.COLOR_BGR2GRAY)
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
            plt.imshow(np.clip(self.transfer_images[i], 0, 255).astype(np.uint8))

        for i in range(15, 30):

            plt.subplot(4, 15, i + 16)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.origin_images[i])

            plt.subplot(4, 15, i + 31)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(np.clip(self.transfer_images[i], 0, 255).astype(np.uint8))

        plt.get_current_fig_manager().window.showMaximized()
        plt.interactive(True)
        plt.show()