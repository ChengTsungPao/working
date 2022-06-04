from model import Network
from inout import load_mnist, preprocess

if __name__ == '__main__':

    '''
        Hyper parameters
        
            - dataset_name              choose between 'mnist' and 'cifar'
            - num_epochs                number of epochs
            - learning_rate             learning rate
            - validate                  0 -> no validation, 1 -> validation
            - regularization            regularization term (i.e., lambda)
            - verbose                   > 0 --> verbosity
            - plot_weights              > 0 --> plot weights distribution
    '''

    num_epochs = 5
    batch_size = 8
    learning_rate = 0.001
    validate = 1
    verbose = 1
    plot_weights = 1

    print('\n--- Loading dataset ---')                 # load dataset
    dataset = load_mnist()

    print('\n--- Processing the dataset ---')                               # pre process dataset
    dataset = preprocess(dataset)

    print('\n--- Building the model ---')                                   # build model
    model = Network()
    model.build_model()

    print('\n--- Training the model ---')                                   # train model
    model.train(
        dataset,
        num_epochs,
        batch_size,
        learning_rate,
        validate,
        plot_weights,
        verbose
    )

    print('\n--- Testing the model ---')                                    # test model
    model.evaluate(
        dataset['test_images'],
        dataset['test_labels'],
        verbose
    )
