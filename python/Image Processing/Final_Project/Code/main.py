from Data_Training import data_training
import numpy as np
import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

    # path = "./Scaphoid/"
    # data_training_fcn = data_training(path)
    # data_training_fcn.train_bounding_box_wider_data()
    # data_training_fcn.train_bounding_box_narrow_data()
    # data_training_fcn.train_classifier_data()
