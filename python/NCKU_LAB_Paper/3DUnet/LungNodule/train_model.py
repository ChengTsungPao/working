from model.create_model import getModel2
import tensorflow as tf
import numpy as np

def get_data(path):
    pass

def predict_model(model):
    image = np.ones((1,) + IMAGE_SPATIAL_DIMS[0] + (IMAGE_NUM_CHANNELS[0],))

    outputs = model(image)
    print("TLF => heatMap    : ", outputs[0].shape)
    print("TLF => group      : ", outputs[1].shape)
    print("TLF => regression : ", outputs[2].shape)
    print("BRB => heatMap    : ", outputs[3].shape)
    print("BRB => group      : ", outputs[4].shape)
    print("BRB => regression : ", outputs[5].shape)

def train():
    IMAGE_SPATIAL_DIMS = [(128, 128, 128), (64, 64, 64)]
    IMAGE_NUM_CHANNELS = [1, 1]

    model = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)

    num_data = 20
    data = np.random.randn(num_data, 1, IMAGE_SPATIAL_DIMS[0][0], IMAGE_SPATIAL_DIMS[0][1], IMAGE_SPATIAL_DIMS[0][2], 1)
    target = np.random.randint(0, IMAGE_SPATIAL_DIMS[1][0], size = (num_data, 2, 1, 5, 3)) # (_, tlf brb, b, bbox num, dim)

    epochs = 2

    loss_fn   = model.loss
    optimizer = model.optimizer

    for epoch in range(epochs):
        print("\nStart of epoch %d" % (epoch,))

        for step, (x_batch_train, y_batch_train) in enumerate(zip(data, target)):

            with tf.GradientTape() as tape:
                predicts = model(x_batch_train, training=True) 
                loss_value = loss_fn(y_batch_train, predicts)

            grads = tape.gradient(loss_value, model.trainable_weights)
            optimizer.apply_gradients(zip(grads, model.trainable_weights))

            print("\r", "Train: %.4f" % (((step + 1) / num_data) * 100.), "%", "(step: {}, loss = {})".format(step, loss_value), end=" ")


if __name__ == "__main__":
    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    train()

