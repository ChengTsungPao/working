from Corner_Detection import corner_detection
from Augmented_Reality import augmented_reality
from Stereo_Disparity_Map import stereo_disparity_map
from Scale_Invariant_Feature_Transform import scale_invariant_feature_transform
from Cifar10_Classifier import cifar10_classifier

import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

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
    # scale_invariant_feature_transform_fcn.matched_images()

    # problem = 5
    # cifar10_classifier_fcn = cifar10_classifier()
    # cifar10_classifier_fcn.plot_Cifa10_images()
    # cifar10_classifier_fcn.show_model_summary()
    # cifar10_classifier_fcn.show_hyperparameters()
    # cifar10_classifier_fcn.train_data()
    # cifar10_classifier_fcn.test_data()
    # cifar10_classifier_fcn.plot_result()

