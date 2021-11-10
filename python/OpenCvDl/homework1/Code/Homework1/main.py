import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    # app = QtWidgets.QApplication(sys.argv)
    # ui = UI()
    # sys.exit(app.exec_())

    from Image_Processing import image_processing
    from Image_Smoothing import image_smoothing
    from Edge_Detection import edge_detection
    from Transforms import transforms

    # path = "./Dataset_OpenCvDl_Hw1/Q1_Image/"
    # image_processing_fcn = image_processing(path)
    # image_processing_fcn.load_image()
    # image_processing_fcn.color_separation()
    # image_processing_fcn.color_transformation()
    # image_processing_fcn.blending()


    # path = "./Dataset_OpenCvDl_Hw1/Q2_Image/"
    # image_smoothing_fcn = image_smoothing(path)
    # image_smoothing_fcn.gaussian_blur()
    # image_smoothing_fcn.bilateral_filter()
    # image_smoothing_fcn.median_filter()


    # path = "./Dataset_OpenCvDl_Hw1/Q3_Image/"
    # edge_detection_fcn = edge_detection(path)
    # edge_detection_fcn.gaussian_blur()
    # edge_detection_fcn.sobelX()
    # edge_detection_fcn.sobelY()
    # edge_detection_fcn.magnitude()


    # path = "./Dataset_OpenCvDl_Hw1/Q4_Image/"
    # transforms_fcn = transforms(path)
    # transforms_fcn.resize()
    # transforms_fcn.translation()
    # transforms_fcn.scaling_rotation()
    # transforms_fcn.shearing()

