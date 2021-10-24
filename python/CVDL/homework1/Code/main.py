from Corner_Detection import corner_detection
from Stereo_Disparity_Map import stereo_disparity_map
import cv2
import numpy as np

if __name__ == "__main__":

    # problem = 1
    # path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
    # corner_detection_fcn = corner_detection(path)
    # corner_detection_fcn.find_corners(True)
    # corner_detection_fcn.find_intrinsic()
    # corner_detection_fcn.find_extrinsic(1)
    # corner_detection_fcn.find_distortion()
    # corner_detection_fcn.show()

    problem = 3
    path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
    stereo_disparity_map_fcn = stereo_disparity_map(path)
    stereo_disparity_map_fcn.stereo_disparity_map()
    stereo_disparity_map_fcn.check_disparity_value()
