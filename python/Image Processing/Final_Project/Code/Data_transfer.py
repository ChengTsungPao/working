from PIL.Image import new
from Data_Reader import data_reader
import numpy as np
import torch
import matplotlib.pylab as plt
from Dataset_Create import dataset_create

class data_transfer(data_reader):

    def __init__(self, path):
        super().__init__(path)
        self.bounding_box_wider_dataset = []


    def convertBoundingBoxToSeg_noRotated(self, image, target):
        top, down, left, right = min(target[1], target[3]), max(target[1], target[3]), min(target[0], target[2]), max(target[0], target[2])

        newImage = np.zeros((image.shape[0], image.shape[1]))
        for i in range(len(newImage)):
            for j in range(len(newImage[0])):
                if top <= i <= down and left <= j <= right:
                    newImage[i][j] = 1
                    # image[i][j] = 1

        # plt.imshow(newImage, cmap="binary")
        # plt.show()        
        # plt.imshow(image, cmap="binary")
        # plt.show()        

        return newImage


    def bounding_box_wider_data_transfer(self):
        
        mask = []
        for index in range(len(self.bounding_box_wider_target)):
            mask.append(self.convertBoundingBoxToSeg_noRotated(self.bounding_box_wider_data[index], self.bounding_box_wider_target[index]))

        self.bounding_box_wider_dataset = dataset_create(self.bounding_box_wider_data, mask)