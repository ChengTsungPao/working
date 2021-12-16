from ASIRRA_Train import ASIRRA_train
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pylab as plt
# from threading import Thread
# from multiprocessing import Process
import os

class ASIRRA_classifier(ASIRRA_train):

    def __init__(self):
        super().__init__()

        self.targetTable = {
            0: "cat",
            1: "dog"
        }


    def show_mode_structure(self):
        print(self.model.summary())


    def show_tensorboard(self):
        if not os.path.exists("./predict/"):
            self.train_origin()

        # Process(target = self.open_tensorboard)
        os.system("start http://localhost:6006/")

    
    def open_tensorboard(self):
        os.system("tensorboard --logdir=predict/")


    def show_test_result(self, index = 1):
        if not self.check_model_exist("origin_model.h5"):
            self.train_origin()

        if self.test_data == []:
            self.get_test_data()
            
        index = (int(index) - 1) % len(self.test_data)
        origin_model = load_model("./model/origin_model.h5")
        predict = origin_model.predict(self.test_data[index].reshape(-1, self.test_data.shape[1], self.test_data.shape[2], self.test_data.shape[3]))
        predict = np.argmax(predict[0])

        plt.title("Class:{}".format(self.targetTable[predict]))
        plt.axis("off")
        plt.imshow(self.test_data[index])
        plt.show()
        

    def show_random_erasing(self):
        if not self.check_model_exist("origin_model.h5"):
            self.train_origin()

        if not self.check_model_exist("augmentation_model.h5"):
            self.train_augmentation()

        if self.test_data == []:
            self.get_test_data()

        origin_model = load_model("./model/origin_model.h5")
        augmentation_model = load_model("./model/augmentation_model.h5")

        origin_model_acc = origin_model.evaluate(self.test_data, to_categorical(self.test_target))[-1]
        augmentation_model_acc = augmentation_model.evaluate(self.test_data, to_categorical(self.test_target))[-1]
        self.plot_accuracy(origin_model_acc, augmentation_model_acc)


    def check_model_exist(self, filename):
        if not os.path.exists("./model/"):
            return False

        return os.path.isfile("./model/{}".format(filename))


    def plot_accuracy(self, origin_model_acc, augmentation_model_acc):
        plt.title("Random-Erasing")
        plt.bar(["Before Random-Erasing", "After Random-Erasing"], [origin_model_acc * 100, augmentation_model_acc * 100])
        plt.ylabel("Accuracy")
        plt.show()


        

