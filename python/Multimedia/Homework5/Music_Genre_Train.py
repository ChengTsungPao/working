from matplotlib.pyplot import axis
from Music_Genre_Dataset import music_genre_dataset

import os
import time
import random
import numpy as np
from multiprocessing import Process
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPooling1D, LayerNormalization, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

physical_devices = tf.config.experimental.list_physical_devices("GPU")
tf.config.experimental.set_memory_growth(physical_devices[0], True)

class music_genre_train:
    def __init__(self, path):
        self.dataset = music_genre_dataset(path)

        self.train_data = []
        self.train_label= []
        self.test_data = []
        self.test_label= []
        
        self.EPOCH = 20
        self.BATCH_SIZE = 4
        self.LR = 0.0001
        self.model = None

    def getModel(self, shape):
        model = Sequential()
        model.add(LayerNormalization())
        model.add(Conv1D(32, 100, activation='relu',input_shape=shape[1:]))
        model.add(MaxPooling1D(2))
        model.add(Conv1D(64, 100, activation='relu'))
        model.add(MaxPooling1D(2))
        model.add(Flatten())
        model.add(Dense(128, activation="relu"))
        model.add(Dense(10, activation="softmax"))
        return model

    def getOriginData(self, foldIndex):
        if self.dataset.datas == []:
            self.dataset.readOriginData()

        n = len(self.dataset.datas)
        size = int(n * 0.2)

        randomIndex = list(range(n))
        random.shuffle(randomIndex)

        trainDataIndex = np.array(list(randomIndex[:size * foldIndex]) + list(randomIndex[size * (foldIndex + 1):]))
        testDataIndex = randomIndex[size * foldIndex: size * (foldIndex + 1)]

        self.train_data, self.train_label = self.dataset.datas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.datas[testDataIndex], self.dataset.labels[testDataIndex]
        train_shape = (-1, self.train_data.shape[1], 1)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def getFFTData(self, foldIndex):
        if self.dataset.FFTDatas == []:
            self.dataset.transferFFTData()

        n = len(self.dataset.datas)
        size = int(n * 0.2)

        randomIndex = list(range(n))
        random.shuffle(randomIndex)

        trainDataIndex = np.array(list(randomIndex[:size * foldIndex]) + list(randomIndex[size * (foldIndex + 1):]))
        testDataIndex = randomIndex[size * foldIndex: size * (foldIndex + 1)]

        self.train_data, self.train_label = self.dataset.FFTDatas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.FFTDatas[testDataIndex], self.dataset.labels[testDataIndex]
        train_shape = (-1, self.train_data.shape[1], 1)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def train(self, isOriginData = True):

        for foldIndex in range(5):
            p = Process(target = self.train_helper, args = (foldIndex, isOriginData,))
            p.start()
            p.join()

    def train_helper(self, foldIndex, isOriginData):

        now = time.localtime(time.time())
        currentTime = "{}_{}{}_{}{}".format(now.tm_year, str(now.tm_mon).zfill(2), str(now.tm_mday).zfill(2), str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2))

        if isOriginData:
            self.getOriginData(foldIndex)
        else:
            self.getFFTData(foldIndex)

        self.model = self.getModel(self.train_data.shape)
        self.model.compile(optimizer = Adam(learning_rate=self.LR), loss = "categorical_crossentropy", metrics = ["acc"])

        H = self.model.fit(
            self.train_data, 
            to_categorical(self.train_label), 
            validation_data = [self.test_data, to_categorical(self.test_label)], 
            epochs = self.EPOCH, 
            batch_size = self.BATCH_SIZE, 
            shuffle = True
        )
        print("############################### Accuracy = {} ###############################".format(str(H.history["val_acc"][-1])))

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        self.model.save("./model/{}_model{}.h5".format(currentTime, foldIndex + 1))

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")
        np.savez("./predict/{}_loss{}.npz".format(currentTime, foldIndex + 1), train_loss = H.history["loss"], test_loss = H.history["val_loss"])
        np.savez("./predict/{}_accuracy{}.npz".format(currentTime, foldIndex + 1), train_accuracy = H.history["acc"], test_accuracy = H.history["val_acc"])