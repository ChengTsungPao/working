import tensorflow as tf
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Activation
from tensorflow.keras import Model
import os


def ResNet50():

    resnet = tf.keras.applications.resnet50.ResNet50(include_top = False, weights = "imagenet", classes = 2)
    layer = resnet.output
    layer = GlobalAveragePooling2D() (layer)
    layer = Dense(2048, activation = "relu") (layer)
    layer = Dense(2, activation = "softmax") (layer)
    model = Model(inputs = resnet.input, outputs = layer)

    os.system("cls||clear")

    return model
