from Corner_Detection import corner_detection
from Augmented_Reality import augmented_reality
from Stereo_Disparity_Map import stereo_disparity_map
from Scale_Invariant_Feature_Transform import scale_invariant_feature_transform
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

    problem = 2
    path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
    augmented_reality_fcn = augmented_reality(path)

    # problem = 3
    # path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
    # stereo_disparity_map_fcn = stereo_disparity_map(path)
    # stereo_disparity_map_fcn.stereo_disparity_map()
    # stereo_disparity_map_fcn.check_disparity_value()

    # problem = 4
    # path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
    # scale_invariant_feature_transform_fcn = scale_invariant_feature_transform(path)
    # scale_invariant_feature_transform_fcn.find_keypoints()
    # scale_invariant_feature_transform_fcn.matched_keypoints()
