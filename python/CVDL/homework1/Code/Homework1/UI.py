from Corner_Detection import corner_detection
from Augmented_Reality import augmented_reality
from Stereo_Disparity_Map import stereo_disparity_map
from Scale_Invariant_Feature_Transform import scale_invariant_feature_transform

from PyQt5 import QtWidgets, uic


class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        # Image and Library Path
        self.path = ".//Dataset_CvDl_Hw1//Q{}_Image//"
        
        # problem 1 UI connect
        self.corner_detection_fcn = None
        self.Find_Corners.clicked.connect(self.find_corners)
        self.Find_Intrinsic.clicked.connect(self.find_intrinsic)
        self.Find_Extrinsic.clicked.connect(self.find_extrinsic)
        self.Find_Distortion.clicked.connect(self.find_distortion)
        self.Show_Result.clicked.connect(self.show_result)

        # problem 2 UI connect
        self.augmented_reality_fcn = None
        self.Show_Words_on_Board.clicked.connect(self.draw_board)
        self.Show_Words_Vertically.clicked.connect(self.draw_vertical)
        
        # problem = 3 UI connect
        self.stereo_disparity_map_fcn = None
        self.Stereo_Disparity_Map.clicked.connect(self.stereo_disparity_map)

        # problem = 4 UI connect
        self.scale_invariant_feature_transform_fcn = None
        self.Keypoints.clicked.connect(self.find_keypoints)
        self.Matched_keypoints.clicked.connect(self.matched_keypoints)
        self.Warp_Image.clicked.connect(self.matched_images)

        self.show()

    # setup function
    def setup_camera_calibration(self):
        self.corner_detection_fcn = corner_detection_fcn = corner_detection(self.path.format(1))

    def setup_augmented_reality(self):
        self.augmented_reality_fcn = augmented_reality(self.path.format(2))

    def setup_stereo_disparity_map(self):
        self.stereo_disparity_map_fcn = stereo_disparity_map(self.path.format(3))

    def setup_scale_invariant_feature_transform(self):
        self.scale_invariant_feature_transform_fcn = scale_invariant_feature_transform(self.path.format(4))

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

    # problem 2
    def draw_board(self):
        if self.augmented_reality_fcn == None:
            self.setup_augmented_reality()

        self.augmented_reality_fcn.draw_board(self.AR_InputBox.text())

    def draw_vertical(self):
        if self.augmented_reality_fcn == None:
            self.setup_augmented_reality()

        self.augmented_reality_fcn.draw_vertical(self.AR_InputBox.text())

    # problem 3
    def stereo_disparity_map(self):
        if self.stereo_disparity_map_fcn == None:
            self.setup_stereo_disparity_map()

        self.stereo_disparity_map_fcn.stereo_disparity_map()
        self.stereo_disparity_map_fcn.check_disparity_value()

    # problem 4
    def find_keypoints(self):
        if self.scale_invariant_feature_transform_fcn == None:
            self.setup_scale_invariant_feature_transform()

        self.scale_invariant_feature_transform_fcn.find_keypoints()

    def matched_keypoints(self):
        if self.scale_invariant_feature_transform_fcn == None:
            self.setup_scale_invariant_feature_transform()

        self.scale_invariant_feature_transform_fcn.matched_keypoints()

    def matched_images(self):
        if self.scale_invariant_feature_transform_fcn == None:
            self.setup_scale_invariant_feature_transform()

        self.scale_invariant_feature_transform_fcn.matched_images()