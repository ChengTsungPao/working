from Music_Genre_Dataset import music_genre_dataset
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import numpy as np
import random

class music_genre_regression:
    def __init__(self, path):
        self.dataset = music_genre_dataset(path)

        self.train_data = []
        self.train_label= []
        self.test_data = []
        self.test_label= []

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

        train_shape = (-1,) + (self.train_data.shape[-1],)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def getFFTData(self, foldIndex, shuffleIndexArr):
        if self.dataset.FFTDatas == []:
            self.dataset.transferFFTData()

        trainDataIndex, testDataIndex = self.getSplitIndex(foldIndex, shuffleIndexArr)

        self.train_data, self.train_label = self.dataset.FFTDatas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.FFTDatas[testDataIndex], self.dataset.labels[testDataIndex]

        train_shape = (-1,) + (self.train_data.shape[-1],)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def getSpectrogramData(self, foldIndex, shuffleIndexArr):
        if self.dataset.SpectrogramDatas == []:
            self.dataset.transferSpectrogramData()

        trainDataIndex, testDataIndex = self.getSplitIndex(foldIndex, shuffleIndexArr)

        self.train_data, self.train_label = self.dataset.SpectrogramDatas[trainDataIndex], self.dataset.labels[trainDataIndex]
        self.test_data, self.test_label = self.dataset.SpectrogramDatas[testDataIndex], self.dataset.labels[testDataIndex]

        train_shape = (-1,) + (self.train_data.shape[-1] * self.train_data.shape[-2],)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def train(self):
        
        shuffleIndexArr = self.getShuffleIndexArr()

        for foldIndex in range(5):      
            self.getSpectrogramData(foldIndex, shuffleIndexArr)
            model = LogisticRegression(max_iter = 10).fit(self.train_data, self.train_label)
            print("Accuracy = {}".format(accuracy_score(self.test_label, model.predict(self.test_data))))