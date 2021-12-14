# from ResNet50_Model import ResNet50
import imp
from keras.utils import np_utils

import os
import numpy as np
import matplotlib.pylab as plt
import tensorflow as tf
from tensorflow.python.ops.gen_math_ops import mod
import tensorflow_datasets as tfds
from ResNet50_Model import ResNet50

class ASIRRA_classifier():

    def __init__(self):

        self.train_data = []
        self.train_target = []
        self.val_data = []
        self.val_target = []
        self.test_data = []
        self.test_target = []

        self.train_augmentation_data = []

        self.model = ResNet50()


    def get_data(self):

        def data_transfer(dataset):
            datas, targets = [], []
            for data, target in dataset:
    
                datas.append(data.numpy())
                targets.append(target.numpy())
            return np.array(datas), np.array(targets)

        (training_set, validation_set, test_set), _ = tfds.load('cats_vs_dogs', split=['train[:20%]', 'train[20%:90%]','train[90%:]'], as_supervised = True, with_info = True)

        self.train_data, self.train_target = data_transfer(training_set)
        # self.val_data, self.val_target = data_transfer(validation_set)
        # self.test_data, self.test_target = data_transfer(test_set)


    def data_augmentation(self):
        if self.train_data == []:
            self.get_data()

        # def random_erasing(img, probability = 0.5, sl = 0.02, sh = 0.4, r1 = 0.3):

        #     height = tf.shape(img)[0]
        #     width = tf.shape(img)[1]
        #     channel = tf.shape(img)[2]
        #     area = tf.cast(width*height, tf.float32)

        #     erase_area_low_bound = tf.cast(tf.round(tf.sqrt(sl * area * r1)), tf.int32)
        #     erase_area_up_bound = tf.cast(tf.round(tf.sqrt((sh * area) / r1)), tf.int32)
        #     h_upper_bound = tf.minimum(erase_area_up_bound, height)
        #     w_upper_bound = tf.minimum(erase_area_up_bound, width)

        #     h = tf.random.uniform([], erase_area_low_bound, h_upper_bound, tf.int32)
        #     w = tf.random.uniform([], erase_area_low_bound, w_upper_bound, tf.int32)

        #     x1 = tf.random.uniform([], 0, height+1 - h, tf.int32)
        #     y1 = tf.random.uniform([], 0, width+1 - w, tf.int32)

        #     erase_area = tf.cast(tf.random.uniform([h, w, channel], 0, 255, tf.int32), tf.uint8)
        #     erasing_img = img[x1:x1+h, y1:y1+w, :].assign(erase_area)

        #     return tf.cond(tf.random.uniform([], 0, 1) > probability, lambda: img, lambda: erasing_img)

        def random_erasing(img, probability = 0.5, sl = 0.02, sh = 0.4, r1 = 0.3):
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

        # random_erasing(tf.Variable(data, validate_shape=False))
        self.train_augmentation_data = [random_erasing(data) for data in self.train_data]
        print("Finish !!!")



    def train_augmentation(self):
        if self.train_augmentation_data == []:
            self.data_augmentation()

        self.model.compile(optimizer = "Adam", loss = "categorical_crossentropy", metrics = ["mae", "acc"])
        self.model.fit(self.train_augmentation_data, np_utils.to_categorical(self.train_target), batch_size = 4, epochs = 10, validation_split = 0.8, validation_freq = 2)


    def train_origin(self):
        if self.train_data == []:
            self.get_data()

        self.model.compile(optimizer = "Adam", loss = "categorical_crossentropy", metrics = ["mae", "acc"])
        self.model.fit(self.train_data, np_utils.to_categorical(self.train_target), batch_size = 4, epochs = 10, validation_split = 0.8, validation_freq = 2)

