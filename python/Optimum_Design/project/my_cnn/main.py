from model import Network
from inout import load_mnist, preprocess

if __name__ == '__main__':

    num_epochs = 5
    batch_size = 8
    learning_rate = 0.001
    validate = 1
    verbose = 1

    print('\n--- Loading dataset ---')
    dataset = load_mnist()

    print('\n--- Processing the dataset ---')
    dataset = preprocess(dataset)

    print('\n--- Building the model ---')
    model = Network()
    model.build_model()

    print('\n--- Training the model ---')
    model.train(
        dataset,
        num_epochs,
        batch_size,
        learning_rate,
        validate,
        verbose
    )

    print('\n--- Testing the model ---')
    model.evaluate(
        dataset['test_images'],
        dataset['test_labels'],
        verbose
    )
