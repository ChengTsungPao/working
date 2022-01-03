from numpy.core.fromnumeric import size
from Data_Reader import data_reader
from Config import wider_data_training_size, narrow_data_training_size, classifier_data_training_size
import numpy as np
import torch
import matplotlib.pylab as plt
from Dataset_Create import dataset_create
import cv2
import os

class data_transfer(data_reader):

    def __init__(self, path):
        super().__init__(path)

        self.bounding_box_wider_dataset1 = []
        self.bounding_box_wider_dataset2 = []
        self.bounding_box_wider_dataset3 = []

        self.bounding_box_narrow_dataset1 = []
        self.bounding_box_narrow_dataset2 = []
        self.bounding_box_narrow_dataset3 = []

        self.classifier_dataset1 = []
        self.classifier_dataset2 = []
        self.classifier_dataset3 = []


    def convertBoundingBoxToSeg_noRotated(self, image, target):
        top, down, left, right = min(target[1], target[3]), max(target[1], target[3]), min(target[0], target[2]), max(target[0], target[2])

        newImage = np.zeros((image.shape[0], image.shape[1]))
        for i in range(len(newImage)):
            for j in range(len(newImage[0])):
                if top <= i <= down and left <= j <= right:
                    newImage[i][j] = 1
                    # image[i][j] = 1 # notice: call by reference

        # plt.subplot(121)
        # plt.imshow(newImage, cmap="binary")    
        # plt.subplot(122)
        # plt.imshow(image, cmap="binary")
        # plt.show()       

        return newImage

    def convertBoundingBoxToSeg_rotated(self, image, target):
        shape = image.shape
        rotated_matrix = cv2.getRotationMatrix2D((shape[1] // 2, shape[0] // 2), target[-1], 1)

        point = np.array([[target[0]], [target[1]], [1]])
        point = np.dot(rotated_matrix, point)

        width, height = target[2], target[3]
        top, down, left, right = point[1][0] - height / 2, point[1][0] + height / 2, point[0][0] - width / 2, point[0][0] + width / 2

        newImage = np.zeros((shape[0], shape[1]))
        for i in range(len(newImage)):
            for j in range(len(newImage[0])):
                j_ = rotated_matrix[0][0] * j + rotated_matrix[0][1] * i + rotated_matrix[0][2]
                i_ = rotated_matrix[1][0] * j + rotated_matrix[1][1] * i + rotated_matrix[1][2]
                if top <= i_ <= down and left <= j_ <= right:
                    newImage[i][j] = 1
                    # image[i][j] = 1 # notice: call by reference

        # plt.subplot(121)
        # plt.imshow(newImage, cmap="binary")    
        # plt.subplot(122)
        # plt.imshow(image, cmap="binary")
        # plt.show()        

        return newImage


    def convertClassifierDataSize(self, image):
        return cv2.resize(image, dsize=(classifier_data_training_size, classifier_data_training_size), interpolation=cv2.INTER_LINEAR)


    def bounding_box_wider_data_transfer(self):
        
        images = []
        masks = []
        for index in range(len(self.bounding_box_wider_target)):
            images.append(self.bounding_box_wider_data[index])
            masks.append(self.convertBoundingBoxToSeg_noRotated(self.bounding_box_wider_data[index], self.bounding_box_wider_target[index]))

        images = np.array(images)
        masks = np.array(masks)

        randomIndex = np.arange(len(images))
        np.random.shuffle(randomIndex)
        size = len(randomIndex) // 3

        self.bounding_box_wider_dataset1 = dataset_create(images[randomIndex[: size]], masks[randomIndex[: size]], wider_data_training_size)
        self.bounding_box_wider_dataset2 = dataset_create(images[randomIndex[size : size * 2]], masks[randomIndex[size : size * 2]], wider_data_training_size)
        self.bounding_box_wider_dataset3 = dataset_create(images[randomIndex[size * 2:]], masks[randomIndex[size * 2:]], wider_data_training_size)


    def bounding_box_narrow_data_transfer(self):
        if not os.path.isfile("./predict/bounding_box_wider_data_predict.npz"):
            return

        result = np.load("./predict/bounding_box_wider_data_predict.npz")

        images = []
        masks = []
        for index in range(len(self.bounding_box_narrow_target)):
            x1, y1, x2, y2 = result["predict"][index]
            images.append(np.array(self.bounding_box_narrow_data[index][y1:y2, x1:x2]).astype(np.float64) / 255)
            masks.append(self.convertBoundingBoxToSeg_rotated(self.bounding_box_narrow_data[index][y1:y2, x1:x2], self.bounding_box_narrow_target[index]))

        images = np.array(images)
        masks = np.array(masks)

        randomIndex = np.arange(len(images))
        np.random.shuffle(randomIndex)
        size = len(randomIndex) // 3

        self.bounding_box_narrow_dataset1 = dataset_create(images[randomIndex[: size]], masks[randomIndex[:size]], narrow_data_training_size)
        self.bounding_box_narrow_dataset2 = dataset_create(images[randomIndex[size : size * 2]], masks[randomIndex[size : size * 2]], narrow_data_training_size)
        self.bounding_box_narrow_dataset3 = dataset_create(images[randomIndex[size * 2:]], masks[randomIndex[size * 2:]], narrow_data_training_size)


    def classifier_data_transfer(self):

        result = np.load("./predict/bounding_box_wider_data_predict.npz")

        datas = []
        for index, data in enumerate(self.classifier_data):
            x1, y1, x2, y2 = result["predict"][index]
            datas.append(self.convertClassifierDataSize(data[y1:y2, x1:x2]))

        images = (np.array(datas).astype(np.float64) / 255).transpose((0, 3, 1, 2))
        targets = np.array(self.classifier_target)

        randomIndex = np.arange(len(images))
        np.random.shuffle(randomIndex)
        size = len(randomIndex) // 3

        self.classifier_dataset1 = torch.utils.data.TensorDataset(torch.tensor(images[randomIndex[: size]]), torch.tensor(targets[randomIndex[: size]]))
        self.classifier_dataset2 = torch.utils.data.TensorDataset(torch.tensor(images[randomIndex[size : size * 2]]), torch.tensor(targets[randomIndex[size : size * 2]]))
        self.classifier_dataset3 = torch.utils.data.TensorDataset(torch.tensor(images[randomIndex[size * 2:]]), torch.tensor(targets[randomIndex[size * 2:]]))
