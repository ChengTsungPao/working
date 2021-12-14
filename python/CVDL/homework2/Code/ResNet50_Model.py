from keras.layers import Activation, Dense, GlobalAveragePooling2D
import tensorflow as tf


def ResNet50():

    model = tf.keras.applications.ResNet50(include_top=False, weights="imagenet")
    layer = model.output
    layer = GlobalAveragePooling2D(layer)
    layer = Dense(1024, Activation = "relu")(layer)
    layer = Dense(2, Activation = "relu")(layer)

    return layer