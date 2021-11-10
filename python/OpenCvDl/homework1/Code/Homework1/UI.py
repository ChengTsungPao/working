from Image_Processing import image_processing
from Image_Smoothing import image_smoothing
from Edge_Detection import edge_detection
from Transforms import transforms

from PyQt5 import QtWidgets, uic


class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        # Image and Library Path
        self.path = ".//Dataset_OpenCvDl_Hw1//Q{}_Image//"
        
        # problem 1 UI connect
        self.image_processing_fcn = None
        self.Load_Image.clicked.connect(self.load_image)
        self.Color_Separation.clicked.connect(self.color_separation)
        self.Color_Transformations.clicked.connect(self.color_transformation)
        self.Blending.clicked.connect(self.blending)

        # problem 2 UI connect
        self.image_smoothing_fcn = None
        self.Gaussian_Blur.clicked.connect(self.gaussian_blur)
        self.Bilateral_Filter.clicked.connect(self.bilateral_filter)
        self.Median_Filter.clicked.connect(self.median_filter)
        
        # problem = 3 UI connect
        self.edge_detection_fcn = None
        self.Gaussian_Blur_Self.clicked.connect(self.gaussian_blur_self)
        self.SobelX.clicked.connect(self.sobelX)
        self.SobelY.clicked.connect(self.sobelY)
        self.Magnitude.clicked.connect(self.magnitude)

        # problem = 4 UI connect
        self.transforms_fcn = None
        self.Resize.clicked.connect(self.resizeImage)
        self.Translation.clicked.connect(self.translation)
        self.Rotation_Scaling.clicked.connect(self.scaling_rotation)
        self.Shearing.clicked.connect(self.shearing)

        self.show()

    # setup function
    def setup_image_processing(self):
        self.image_processing_fcn = image_processing(self.path.format(1))

    def setup_image_smoothing(self):
        self.image_smoothing_fcn = image_smoothing(self.path.format(2))

    def setup_edge_detection(self):
        self.edge_detection_fcn = edge_detection(self.path.format(3))

    def setup_transforms(self):
        self.transforms_fcn = transforms(self.path.format(4))

    # problem 1
    def load_image(self):
        if self.image_processing_fcn == None:
            self.setup_image_processing()

        self.image_processing_fcn.load_image()

    def color_separation(self):
        if self.image_processing_fcn == None:
            self.setup_image_processing()

        self.image_processing_fcn.color_separation()

    def color_transformation(self):
        if self.image_processing_fcn == None:
            self.setup_image_processing()

        self.image_processing_fcn.color_transformation()   

    def blending(self):
        if self.image_processing_fcn == None:
            self.setup_image_processing()

        self.image_processing_fcn.blending()  

    # problem 2
    def gaussian_blur(self):
        if self.image_smoothing_fcn == None:
            self.setup_image_smoothing()

        self.image_smoothing_fcn.gaussian_blur()

    def bilateral_filter(self):
        if self.image_smoothing_fcn == None:
            self.setup_image_smoothing()

        self.image_smoothing_fcn.bilateral_filter()

    def median_filter(self):
        if self.image_smoothing_fcn == None:
            self.setup_image_smoothing()

        self.image_smoothing_fcn.median_filter()

    # problem 3
    def gaussian_blur_self(self):
        if self.edge_detection_fcn == None:
            self.setup_edge_detection()

        self.edge_detection_fcn.gaussian_blur()

    def sobelX(self):
        if self.edge_detection_fcn == None:
            self.setup_edge_detection()

        self.edge_detection_fcn.sobelX()

    def sobelY(self):
        if self.edge_detection_fcn == None:
            self.setup_edge_detection()

        self.edge_detection_fcn.sobelY()

    def magnitude(self):
        if self.edge_detection_fcn == None:
            self.setup_edge_detection()

        self.edge_detection_fcn.magnitude()

    # problem 4
    def resizeImage(self):
        if self.transforms_fcn == None:
            self.setup_transforms()

        self.transforms_fcn.resize()

    def translation(self):
        if self.transforms_fcn == None:
            self.setup_transforms()

        self.transforms_fcn.translation()

    def scaling_rotation(self):
        if self.transforms_fcn == None:
            self.setup_transforms()

        self.transforms_fcn.scaling_rotation()

    def shearing(self):
        if self.transforms_fcn == None:
            self.setup_transforms()

        self.transforms_fcn.shearing()