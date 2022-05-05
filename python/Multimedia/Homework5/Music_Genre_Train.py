from Music_Genre_Dataset import music_genre_dataset

import os
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPooling1D
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
        
        self.EPOCH = 100
        self.BATCH_SIZE = 4
        self.model = None

    def getModel(self, shape):
        model = Sequential()
        model.add(Conv1D(16, 100, activation='relu',input_shape=shape[1:]))
        model.add(MaxPooling1D(2))
        model.add(Conv1D(32, 100, activation='relu'))
        model.add(MaxPooling1D(2))
        model.add(Conv1D(64, 100, activation='relu'))
        model.add(MaxPooling1D(2))
        model.add(Flatten())
        model.add(Dense(128, activation="relu"))
        model.add(Dense(10, activation="softmax"))
        return model

    def getData(self):
        self.dataset.readOriginData()

        n = len(self.dataset.datas)
        randomIndex = list(range(n))
        random.shuffle(randomIndex)

        self.train_data, self.train_label = self.dataset.datas[randomIndex][:int(n * 0.8)], self.dataset.labels[randomIndex][:int(n * 0.8)]
        self.test_data, self.test_label = self.dataset.datas[randomIndex][:int(n * 0.2)], self.dataset.labels[randomIndex][:int(n * 0.2)]
        train_shape = (-1, self.train_data.shape[1], 1)
        self.train_data = self.train_data.reshape(train_shape)
        self.test_data = self.test_data.reshape(train_shape)

    def train_origin(self):
        if self.train_data == []:
            self.getData()

        self.model = self.getModel(self.train_data.shape)
        self.model.compile(optimizer = Adam(learning_rate=0.0001), loss = "categorical_crossentropy", metrics = ["acc"])

        H = self.model.fit(
            self.train_data, 
            to_categorical(self.train_label), 
            validation_data = [self.test_data, to_categorical(self.test_label)], 
            epochs = self.EPOCH, 
            batch_size = self.BATCH_SIZE, 
            shuffle = True
        )
        print("Accuracy = {}".format(H.history["val_acc"][-1]))

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        self.model.save("./model/model.h5")

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")
        np.savez("./predict/loss.npz", train_loss = H.history["loss"], test_loss = H.history["val_loss"])
        np.savez("./predict/accuracy.npz", train_accuracy = H.history["acc"], test_accuracy = H.history["val_acc"])