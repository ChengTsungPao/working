from Cifar10_Classifier import cifar10_classifier

import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

    # problem = 5
    # cifar10_classifier_fcn = cifar10_classifier()
    # cifar10_classifier_fcn.plot_Cifa10_images()
    # cifar10_classifier_fcn.show_model_summary()
    # cifar10_classifier_fcn.show_hyperparameters()
    # cifar10_classifier_fcn.train_data()
    # cifar10_classifier_fcn.test_data()
    # cifar10_classifier_fcn.plot_result()

