from Music_Genre_Dataset import music_genre_dataset

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Conv2D, Flatten, MaxPooling1D, MaxPooling2D, LayerNormalization, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

import os
import time
import random
import numpy as np
from multiprocessing import Process

physical_devices = tf.config.experimental.list_physical_devices("GPU")
tf.config.experimental.set_memory_growth(physical_devices[0], True)

class music_genre_train:
    def __init__(self, path):
        self.dataset = music_genre_dataset(path)

        self.train_data = []
        self.train_label= []
        self.test_data = []
        self.test_label= []
        
        self.EPOCH = 200
        self.BATCH_SIZE = 4
        self.LR = 0.000001
        self.model = None
        self.train_kind = {
            0: "Origin",
            1: "FFT",
            2: "Spectrogram"
        }

    def get1DModel(self, shape):
        self.model = Sequential()
        self.model.add(LayerNormalization())
        self.model.add(Conv1D(32, 100, activation='relu',input_shape=shape[1:]))
        self.model.add(MaxPooling1D(2))
        self.model.add(Conv1D(64, 100, activation='relu'))
        self.model.add(MaxPooling1D(2))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(10, activation="softmax"))

    def get2DModel(self, shape):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=shape[1:]))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dense(10, activation='softmax'))

    def getShuffleIndexArr(self):
        if self.dataset.datas == []:
            self.dataset.readOriginData()

        n = len(self.dataset.labels)
        size = n // 10

        shuffleIndexArr = []
        for i in range(10):
            shuffleIndexArr.append(list(range(i * size, (i + 1) * size)))
            random.shuffle(shuffleIndexArr[-1])

        return shuffleIndexArr

    def getSplitIndex(self, foldIndex, shuffleIndexArr):
        patch = len(shuffleIndexArr[0]) // 5
        trainDataIndex = []
        testDataIndex = []

        for i in range(10):
            trainDataIndex += list(shuffleIndexArr[i][:patch * foldIndex]) + list(shuffleIndexArr[i][patch * (foldIndex + 1):])
            testDataIndex += list(shuffleIndexArr[i][patch * foldIndex: patch * (foldIndex + 1)])

        return np.array(trainDataIndex), np.array(testDataIndex)

    def getOriginData(self, foldIndex, shuffleIndexArr):
        if self.dataset.datas == []:
            self.dataset.readOriginData()

        trainDataIndex, testDataIndex = self.getSplitIndex(foldIndex, shuffleIndexArr)

        self.train_data, self.train_label = self.dataset.datas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.datas[testDataIndex], self.dataset.labels[testDataIndex]

        train_shape = (-1,) + self.train_data.shape[1:] + (1,)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def getFFTData(self, foldIndex, shuffleIndexArr):
        if self.dataset.FFTDatas == []:
            self.dataset.transferFFTData()

        trainDataIndex, testDataIndex = self.getSplitIndex(foldIndex, shuffleIndexArr)

        self.train_data, self.train_label = self.dataset.FFTDatas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.FFTDatas[testDataIndex], self.dataset.labels[testDataIndex]

        train_shape = (-1,) + self.train_data.shape[1:] + (1,)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def getSpectrogramData(self, foldIndex, shuffleIndexArr):
        if self.dataset.SpectrogramDatas == []:
            self.dataset.transferSpectrogramData()

        trainDataIndex, testDataIndex = self.getSplitIndex(foldIndex, shuffleIndexArr)

        self.train_data, self.train_label = self.dataset.SpectrogramDatas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.SpectrogramDatas[testDataIndex], self.dataset.labels[testDataIndex]

        train_shape = (-1,) + self.train_data.shape[1:] + (1,)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def train(self, kindIndex = 0):

        shuffleIndexArr = self.getShuffleIndexArr()

        now = time.localtime(time.time())
        currentTime = "{}_{}{}_{}{}".format(now.tm_year, str(now.tm_mon).zfill(2), str(now.tm_mday).zfill(2), str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2))

        for foldIndex in range(5):
            p = Process(target = self.train_helper, args = (foldIndex, kindIndex, shuffleIndexArr, currentTime,))
            p.start()
            p.join()

    def train_helper(self, foldIndex, kindIndex, shuffleIndexArr, currentTime):

        # Load Data & Build Model
        if kindIndex == 0:
            self.getOriginData(foldIndex, shuffleIndexArr)
            self.get1DModel(self.train_data.shape)
        elif kindIndex == 1:
            self.getFFTData(foldIndex, shuffleIndexArr)
            self.get1DModel(self.train_data.shape)
        else:
            self.getSpectrogramData(foldIndex, shuffleIndexArr)
            self.get2DModel(self.train_data.shape)            
        
        self.model.compile(optimizer = Adam(learning_rate=self.LR), loss = "categorical_crossentropy", metrics = ["acc"])

        H = self.model.fit(
            self.train_data, 
            to_categorical(self.train_label), 
            validation_data = [self.test_data, to_categorical(self.test_label)], 
            epochs = self.EPOCH, 
            batch_size = self.BATCH_SIZE, 
            shuffle = True
        )

        print("############################### Accuracy = {} ###############################\n".format(str(H.history["val_acc"][-1])))

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        self.model.save("./model/{}_{}_model{}.h5".format(currentTime, self.train_kind[kindIndex], foldIndex + 1))

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")
        np.savez("./predict/{}_{}_loss{}.npz".format(currentTime, self.train_kind[kindIndex], foldIndex + 1), train_loss = H.history["loss"], test_loss = H.history["val_loss"])
        np.savez("./predict/{}_{}_accuracy{}.npz".format(currentTime, self.train_kind[kindIndex], foldIndex + 1), train_accuracy = H.history["acc"], test_accuracy = H.history["val_acc"])