from Cifar10_Classifier import cifar10_classifier

if __name__ == "__main__":

    problem = 5
    cifar10_classifier_fcn = cifar10_classifier()
    cifar10_classifier_fcn.plot_Cifa10_images()
    cifar10_classifier_fcn.show_model_summary()
    cifar10_classifier_fcn.show_hyperparameters()
    # cifar10_classifier_fcn.train_data()
    cifar10_classifier_fcn.test_data()
    cifar10_classifier_fcn.plot_result()

