from PCA import pca
from ASIRRA_Classifier import ASIRRA_classifier

if __name__ == "__main__":

    # path = ".//Dataset_CvDl_Hw2//Q4_Image//"
    # pca_fcn = pca(path)
    # pca_fcn.image_reconstruction()
    # pca_fcn.compute_reconstruction_error()


    ASIRRA_classifier_fcn = ASIRRA_classifier()
    ASIRRA_classifier_fcn.train_augmentation()
    # ASIRRA_classifier_fcn.train_origin()