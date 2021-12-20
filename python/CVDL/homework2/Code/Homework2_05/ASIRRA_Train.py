# from ResNet50_Model import ResNet50
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

import os
import cv2
import numpy as np
import matplotlib.pylab as plt
import tensorflow_datasets as tfds
from ResNet50_Model import ResNet50
import warnings
import datetime

warnings.filterwarnings("ignore")

class ASIRRA_train():

    def __init__(self):

        self.train_data = []
        self.train_target = []
        self.val_data = []
        self.val_target = []
        self.test_data = []
        self.test_target = []

        self.train_augmentation_data = []

        self.EPOCH = 15
        self.BATCH_SIZE = 32
        self.model = ResNet50()
        

    def data_resize(self, image):
        return cv2.resize(image, dsize=(224, 224), interpolation=cv2.INTER_LINEAR)


    def data_transfer(self, dataset):
        datas, targets = [], []
        for data, target in dataset:
            datas.append(self.data_resize(data.numpy()))
            targets.append(target.numpy())
        return np.array(datas), np.array(targets)


    def get_train_data(self):

        dataset_split = [
            tfds.Split.TRAIN.subsplit(tfds.percent[:70]),
            tfds.Split.TRAIN.subsplit(tfds.percent[70:90]),
        ]

        [training_set, validation_set] = tfds.load('cats_vs_dogs', split = dataset_split, as_supervised = True)

        self.train_data, self.train_target = self.data_transfer(training_set)
        self.val_data, self.val_target = self.data_transfer(validation_set)

        os.system("cls||clear")


    def get_test_data(self):

        dataset_split = [
            tfds.Split.TRAIN.subsplit(tfds.percent[90:])
        ]

        [test_set] = tfds.load('cats_vs_dogs', split = dataset_split, as_supervised = True)

        self.test_data, self.test_target = self.data_transfer(test_set)

        os.system("cls||clear")


    def random_erasing(self, img, probability = 0.5, sl = 0.02, sh = 0.4, r1 = 0.3):
        height = img.shape[0]
        width = img.shape[1]
        channel = img.shape[2]
        area = width * height

        erase_area_low_bound = np.round( np.sqrt(sl * area * r1) ).astype(np.int)
        erase_area_up_bound = np.round( np.sqrt((sh * area) / r1) ).astype(np.int)
        if erase_area_up_bound < height:
            h_upper_bound = erase_area_up_bound
        else:
            h_upper_bound = height
        if erase_area_up_bound < width:
            w_upper_bound = erase_area_up_bound
        else:
            w_upper_bound = width

        h = np.random.randint(erase_area_low_bound, h_upper_bound)
        w = np.random.randint(erase_area_low_bound, w_upper_bound)

        x1 = np.random.randint(0, height+1 - h)
        y1 = np.random.randint(0, width+1 - w)

        x1 = np.random.randint(0, height - h)
        y1 = np.random.randint(0, width - w)
        img[x1:x1+h, y1:y1+w, :] = np.random.randint(0, 255, size=(h, w, channel)).astype(np.uint8)

        return img


    def data_augmentation(self):
        if self.train_data == []:
            self.get_train_data()

        # random_erasing(tf.Variable(data, validate_shape=False))
        self.train_augmentation_data = np.array([self.random_erasing(data) for data in self.train_data])
        os.system("cls||clear")


    def train_origin(self):
        if self.train_data == []:
            self.get_train_data()
        
        logdir = os.path.join("predict", datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-origin_image")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq = 1)
        
        self.model = ResNet50()
        self.model.compile(optimizer = "Adam", loss = "categorical_crossentropy", metrics = ["acc"])

        H = self.model.fit(
            self.train_data, 
            to_categorical(self.train_target), 
            validation_data = [self.val_data, to_categorical(self.val_target)], 
            callbacks=[tensorboard_callback], 
            epochs = self.EPOCH, 
            batch_size = self.BATCH_SIZE, 
            shuffle=True
        )
        print(H.history["val_acc"][-1])

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        self.model.save("./model/origin_model.h5")


    def train_augmentation(self):
        if self.train_augmentation_data == []:
            self.data_augmentation()

        logdir = os.path.join("predict", datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-augmentation_image")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq = 1)

        self.model = ResNet50()
        self.model.compile(optimizer = "Adam", loss = "categorical_crossentropy", metrics = ["acc"])

        H = self.model.fit(
            self.train_augmentation_data, 
            to_categorical(self.train_target), 
            validation_data = [self.val_data, to_categorical(self.val_target)], 
            callbacks=[tensorboard_callback],
            epochs = self.EPOCH, 
            batch_size = self.BATCH_SIZE, 
            shuffle = True
        )
        print(H.history["val_acc"][-1])

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        self.model.save("./model/augmentation_model.h5")
