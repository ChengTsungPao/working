from layers import Convolutional, Pooling, FullyConnected, Dense, cross_entropy, lr_schedule
from inout import plot_learning_curve, plot_accuracy_curve, plot_histogram
import numpy as np
import time


class Network:
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def build_model(self):
        self.add_layer(Convolutional(name='conv1', num_filters=8, stride=2, size=3, activation='relu'))
        self.add_layer(Convolutional(name='conv2', num_filters=8, stride=2, size=3, activation='relu'))
        self.add_layer(Dense(name='dense', nodes=8 * 6 * 6, num_classes=10))

    def forward(self, images):                # forward propagate
        for layer in self.layers:
            images = layer.forward(images)
        return images

    def backward(self, gradients, learning_rate):                # backward propagate
        for layer in reversed(self.layers):
            gradients = layer.backward(gradients, learning_rate)

    def train(self, dataset, num_epochs, batch_size, learning_rate, validate, plot_weights, verbose):
        history = {'loss': [], 'accuracy': [], 'val_loss': [], 'val_accuracy': []}
        for epoch in range(1, num_epochs + 1):
            print('\n--- Epoch {0} ---'.format(epoch))
            loss, tmp_loss, num_corr = 0, 0, 0
            initial_time = time.time()
            for i in range(0, len(dataset['train_images']), batch_size):
                if i > 0 and i % 5000 == 0:
                    accuracy = (num_corr / (i + 1)) * 100       # compute training accuracy and loss up to iteration i
                    loss = tmp_loss / (i + 1)

                    history['loss'].append(loss)                # update history
                    history['accuracy'].append(accuracy)

                    if validate:
                        indices = np.random.permutation(dataset['validation_images'].shape[0])
                        val_loss, val_accuracy = self.evaluate(
                            dataset['validation_images'][indices, :],
                            dataset['validation_labels'][indices],
                            verbose=0
                        )
                        history['val_loss'].append(val_loss)
                        history['val_accuracy'].append(val_accuracy)

                        if verbose:
                            print('[Step %05d]: Loss %02.3f | Accuracy: %02.3f | Time: %02.2f seconds | '
                                  'Validation Loss %02.3f | Validation Accuracy: %02.3f' %
                                  (i + 1, loss, accuracy, time.time() - initial_time, val_loss, val_accuracy))
                    elif verbose:
                        print('[Step %05d]: Loss %02.3f | Accuracy: %02.3f | Time: %02.2f seconds' %
                              (i + 1, loss, accuracy, time.time() - initial_time))

                    # restart time
                    initial_time = time.time()

                images = dataset['train_images'][i: i + batch_size]
                labels = dataset['train_labels'][i: i + batch_size]

                output = self.forward(images)       # forward propagation

                # compute (regularized) cross-entropy and update loss
                gradient = np.zeros((batch_size, 10), float)
                
                for b in range(batch_size):
                    label = labels[b]
                    tmp_output = output[b]
                    tmp_loss += cross_entropy(tmp_output[label])

                    if np.argmax(tmp_output) == label:                          # update accuracy
                        num_corr += 1

                    gradient[b][label] = -1 / tmp_output[label]

                self.backward(gradient, learning_rate)                      # backward propagation

            learning_rate = lr_schedule(learning_rate, epoch)     # learning rate decay

        if verbose:
            print('Train Loss: %02.3f' % (history['loss'][-1]))
            print('Train Accuracy: %02.3f' % (history['accuracy'][-1]))
            plot_learning_curve(history['loss'])
            plot_accuracy_curve(history['accuracy'], history['val_accuracy'])

        if plot_weights:
            for layer in self.layers:
                if 'pool' not in layer.name:
                    plot_histogram(layer.name, layer.get_weights())

    def evaluate(self, X, y, verbose):
        loss, num_correct = 0, 0
        for i in range(len(X)):
            tmp_output = self.forward(X[i: i + 1])[0]
            loss += cross_entropy(tmp_output[y[i]])

            prediction = np.argmax(tmp_output)
            num_correct += prediction == y[i]

        test_size = len(X)
        accuracy = (num_correct / test_size) * 100
        loss = loss / test_size
        if verbose:
            print('Test Loss: %02.3f' % loss)
            print('Test Accuracy: %02.3f' % accuracy)
        return loss, accuracy
