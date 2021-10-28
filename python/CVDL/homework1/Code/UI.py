from Corner_Detection import corner_detection
from Augmented_Reality import augmented_reality

from PyQt5 import QtWidgets, uic


class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)
        
        # problem 1 UI connect
        self.corner_detection_fcn = None
        self.Find_Corners.clicked.connect(self.find_corners)
        self.Find_Intrinsic.clicked.connect(self.find_intrinsic)
        self.Find_Extrinsic.clicked.connect(self.find_extrinsic)
        self.Find_Distortion.clicked.connect(self.find_distortion)
        self.Show_Result.clicked.connect(self.show_result)
        # problem 2 UI connect
        self.augmented_reality_fcn = None
        # problem = 2
        # path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
        # word = "OPENCV"
        # augmented_reality_fcn = augmented_reality(path)
        # augmented_reality_fcn.draw_board(word)
        # augmented_reality_fcn.draw_vertical(word)

        self.show()

    # setup function
    def setup_camera_calibration(self):
        problem = 1
        path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
        self.corner_detection_fcn = corner_detection_fcn = corner_detection(path)

    def setup_augmented_reality(self):
        problem = 2
        path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
        augmented_reality_fcn = augmented_reality(path)

    # problem 1
    def find_corners(self):
        if self.corner_detection_fcn == None:
            self.setup_camera_calibration()

        self.corner_detection_fcn.find_corners()

    def find_intrinsic(self):
        if self.corner_detection_fcn == None:
            self.setup_camera_calibration()

        self.corner_detection_fcn.find_intrinsic()

    def find_extrinsic(self):
        if self.corner_detection_fcn == None:
            self.setup_camera_calibration()

        self.corner_detection_fcn.find_extrinsic(self.Calibration_InputBox.text())   

    def find_distortion(self):
        if self.corner_detection_fcn == None:
            self.setup_camera_calibration()

        self.corner_detection_fcn.find_distortion()  

    def show_result(self):
        if self.corner_detection_fcn == None:
            self.setup_camera_calibration()

        self.corner_detection_fcn.show()        