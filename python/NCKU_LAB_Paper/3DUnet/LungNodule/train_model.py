from model.create_model import getModel2
import tensorflow as tf
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def get_data(path):
    pass

def train():
    IMAGE_SPATIAL_DIMS = [(64, 64, 64), (64, 64, 64)]
    IMAGE_NUM_CHANNELS = [1, 1]

    model, loss_fn = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)
    # image = np.ones((1,) + IMAGE_SPATIAL_DIMS[0] + (IMAGE_NUM_CHANNELS[0],))

    # outputs = model(image)
    # print("TLF => heatMap    : ", outputs[0].shape)
    # print("TLF => group      : ", outputs[1].shape)
    # print("TLF => regression : ", outputs[2].shape)
    # print("BRB => heatMap    : ", outputs[3].shape)
    # print("BRB => group      : ", outputs[4].shape)
    # print("BRB => regression : ", outputs[5].shape)

    num_data = 100
    data = np.ones((num_data, 1, 64, 64, 64, 1))
    target = np.random.randint(0, 64, size = (num_data, 2, 1, 5, 3)) # (_, tlf brb, b, bbox num, dim)
    train_dataset = zip(data, target)

    epochs = 10
    batch_size = 1
    optimizer = tf.keras.optimizers.SGD(learning_rate=1e-3)

    for epoch in range(epochs):
        print("\nStart of epoch %d" % (epoch,))

        for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):
            print("\r", "Train: %.4f" % ((step / num_data) * 100.), "%", "(step: {})".format(step), end=" ")

            with tf.GradientTape() as tape:
                predicts = model(x_batch_train, training=True) 
                loss_value = loss_fn(y_batch_train, predicts)

            grads = tape.gradient(loss_value, model.trainable_weights)
            optimizer.apply_gradients(zip(grads, model.trainable_weights))

            if step % 10 == 0:
                print("Training loss (for one batch) at step %d: %.4f" % (step, float(loss_value)))
                print("Seen so far: %s samples" % ((step + 1) * batch_size))


if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    train()

