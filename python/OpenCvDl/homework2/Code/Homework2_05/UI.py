from ASIRRA_Classifier import ASIRRA_classifier
from PyQt5 import QtWidgets, uic

class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        # problem 5 UI connect
        self.ASIRRA_classifier_fcn = None
        self.Show_Model_Structure.clicked.connect(self.show_model_structure)
        self.Show_TensorBoard.clicked.connect(self.show_tensorBoard)
        self.Test.clicked.connect(self.test_data)
        self.Random_Erasing.clicked.connect(self.random_erasing)
        self.Train.clicked.connect(self.train_data)

        self.show()

    # setup function
    def setup_ASIRRA_classifier(self):
        self.ASIRRA_classifier_fcn = ASIRRA_classifier()

    # problem 5
    def show_model_structure(self):
        if self.ASIRRA_classifier_fcn == None:
            self.setup_ASIRRA_classifier()

        self.ASIRRA_classifier_fcn.show_mode_structure()

    def show_tensorBoard(self):
        if self.ASIRRA_classifier_fcn == None:
            self.setup_ASIRRA_classifier()

        self.ASIRRA_classifier_fcn.show_tensorboard()

    def test_data(self):
        if self.ASIRRA_classifier_fcn == None:
            self.setup_ASIRRA_classifier()

        self.ASIRRA_classifier_fcn.show_test_result(self.Test_Result_InputBox.text())

    def random_erasing(self):
        if self.ASIRRA_classifier_fcn == None:
            self.setup_ASIRRA_classifier()

        self.ASIRRA_classifier_fcn.show_random_erasing()

    def train_data(self):
        if self.ASIRRA_classifier_fcn == None:
            self.setup_ASIRRA_classifier()

        self.ASIRRA_classifier_fcn.train_origin()
        self.ASIRRA_classifier_fcn.train_augmentation()