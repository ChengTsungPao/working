from Cifar10_Classifier import cifar10_classifier

from PyQt5 import QtWidgets, uic


class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        # problem 5 UI connect
        self.cifar10_classifier_fcn = None
        self.Show_Train_Images.clicked.connect(self.plot_Cifa10_images)
        self.Show_HyperParameter.clicked.connect(self.show_hyperParameters)
        self.Show_Model_Shortcut.clicked.connect(self.show_model_summary)
        self.Show_Accuracy.clicked.connect(self.plot_result)
        self.Test.clicked.connect(self.test_data)
        self.Train.clicked.connect(self.train_data)

        self.show()

    # setup function
    def setup_cifar10_classifier(self):
        self.cifar10_classifier_fcn = cifar10_classifier()

    # problem 5
    def plot_Cifa10_images(self):
        if self.cifar10_classifier_fcn == None:
            self.setup_cifar10_classifier()

        self.cifar10_classifier_fcn.plot_Cifa10_images()

    def show_hyperParameters(self):
        if self.cifar10_classifier_fcn == None:
            self.setup_cifar10_classifier()

        self.cifar10_classifier_fcn.show_hyperParameters()
        
    def show_model_summary(self):
        if self.cifar10_classifier_fcn == None:
            self.setup_cifar10_classifier()

        self.cifar10_classifier_fcn.show_model_summary()

    def plot_result(self):
        if self.cifar10_classifier_fcn == None:
            self.setup_cifar10_classifier()

        self.cifar10_classifier_fcn.plot_result()

    def test_data(self):
        if self.cifar10_classifier_fcn == None:
            self.setup_cifar10_classifier()

        self.cifar10_classifier_fcn.test_data(self.Test_Result_InputBox.text())

    def train_data(self):
        if self.cifar10_classifier_fcn == None:
            self.setup_cifar10_classifier()

        self.cifar10_classifier_fcn.train_data()