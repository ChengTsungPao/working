from ASIRRA_Classifier import ASIRRA_classifier

if __name__ == "__main__":

    ASIRRA_classifier_fcn = ASIRRA_classifier()
    # ASIRRA_classifier_fcn.train_origin()
    # ASIRRA_classifier_fcn.train_augmentation()
    ASIRRA_classifier_fcn.show_mode_structure()
    ASIRRA_classifier_fcn.show_tensorboard()
    ASIRRA_classifier_fcn.show_test_result(1)
    ASIRRA_classifier_fcn.show_random_erasing()