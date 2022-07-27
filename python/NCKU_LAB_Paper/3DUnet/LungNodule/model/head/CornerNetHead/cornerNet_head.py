import tensorflow as tf
import numpy as np

def TopPool(inputs):
    dim = 1
    height = inputs.shape[dim]
    outputs = tf.expand_dims(inputs[:, height - 1, :, :, :], dim)
    for h in range(height - 2, -1, -1):
        new = tf.expand_dims(tf.maximum(outputs[:, 0, :, :, :], inputs[:, h, :, :, :]), dim)
        outputs=tf.concat((new, outputs), dim)
    return outputs
    
def BottomPool(inputs):
    dim = 1
    height = inputs.shape[dim]
    outputs = tf.expand_dims(inputs[:, 0, :, :, :], dim)
    for h in range(1, height):
        new = tf.expand_dims(tf.maximum(outputs[:, -1, :, :, :], inputs[:, h, :, :, :]), dim)
        outputs=tf.concat((outputs, new), dim)
    return outputs

def LeftPool(inputs):
    dim = 2
    width = inputs.shape[dim]
    outputs = tf.expand_dims(inputs[:, :, width - 1, :, :], dim)
    for w in range(width - 2, -1, -1):
        new = tf.expand_dims(tf.maximum(outputs[:, :, 0, :, :], inputs[:, :, w, :, :]), dim)
        outputs=tf.concat((new, outputs), dim)
    return outputs

def RightPool(inputs):
    dim = 2
    width = inputs.shape[dim]
    outputs = tf.expand_dims(inputs[:, :, 0, :, :], dim)
    for w in range(1, width):
        new = tf.expand_dims(tf.maximum(outputs[:, :, -1, :, :], inputs[:, :, w, :, :]), dim)
        outputs=tf.concat((outputs, new), dim)
    return outputs

def FrontPool(inputs):
    dim = 3
    depth = inputs.shape[dim]
    outputs = tf.expand_dims(inputs[:, :, :, depth - 1, :], dim)
    for d in range(depth - 2, -1, -1):
        new = tf.expand_dims(tf.maximum(outputs[:, :, :, 0, :], inputs[:, :, :, d, :]), dim)
        outputs=tf.concat((new, outputs), dim)
    return outputs

def BehindPool(inputs):
    dim = 3
    depth = inputs.shape[dim]
    outputs = tf.expand_dims(inputs[:, :, :, 0, :], dim)
    for d in range(1, depth):
        new = tf.expand_dims(tf.maximum(outputs[:, :, :, -1, :], inputs[:, :, :, d, :]), dim)
        outputs=tf.concat((outputs, new), dim)
    return outputs

class Pool(tf.keras.Model):
    def __init__(self, pool1, pool2, pool3, channel):
        super().__init__()
        self.p1_conv1 = tf.keras.Sequential(
            [
                tf.keras.layers.Conv3D(channel, 3, activation = 'relu', padding = 'same'),
                tf.keras.layers.BatchNormalization(axis=-1)
            ]
        )
        self.p2_conv1 = tf.keras.Sequential(
            [
                tf.keras.layers.Conv3D(channel, 3, activation = 'relu', padding = 'same'),
                tf.keras.layers.BatchNormalization(axis=-1)
            ]
        )
        self.p3_conv1 = tf.keras.Sequential(
            [
                tf.keras.layers.Conv3D(channel, 3, activation = 'relu', padding = 'same'),
                tf.keras.layers.BatchNormalization(axis=-1)
            ]
        )

        self.p_conv1 = tf.keras.layers.Conv3D(channel, 3, activation = 'relu', padding = 'same')
        self.p_bn1   = tf.keras.layers.BatchNormalization(axis=-1)

        self.conv1 = tf.keras.layers.Conv3D(channel, 1, activation = 'relu', padding = 'same')
        self.bn1   = tf.keras.layers.BatchNormalization(axis=-1)

        self.conv2 = tf.keras.Sequential(
            [
                tf.keras.layers.Conv3D(channel, 3, activation = 'relu', padding = 'same'),
                tf.keras.layers.BatchNormalization(axis=-1)
            ]
        )

        self.pool1 = pool1
        self.pool2 = pool2
        self.pool3 = pool3

    def call(self, x):
        # pool 1
        p1_conv1 = self.p1_conv1(x)
        pool1    = self.pool1(p1_conv1)

        # pool 2
        p2_conv1 = self.p2_conv1(x)
        pool2    = self.pool2(p2_conv1)

        # pool 3
        p2_conv1 = self.p3_conv1(x)
        pool3    = self.pool3(p2_conv1)

        # pool 1 + pool 2 + pool 3
        p_conv1 = self.p_conv1(pool1 + pool2 + pool3)
        p_bn1   = self.p_bn1(p_conv1)

        conv1 = self.conv1(x)
        bn1   = self.bn1(conv1)

        conv2 = self.conv2(p_bn1 + bn1)
        return conv2


def cornerPoolingModule(image_spatial_dim, image_num_channels, pool = [TopPool, LeftPool, FrontPool]):

    poolingModule = Pool(pool[0], pool[1], pool[2], image_num_channels)

    inputs  = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,))
    outputs = poolingModule(inputs)

    model = tf.keras.models.Model(inputs, outputs)
    return model


def predictionModule(image_spatial_dim, image_num_channels):

    inputs  = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,))

    heatMap = tf.keras.layers.Conv3D(image_num_channels * 2, 3, activation = 'relu', padding = 'same')(inputs)
    heatMap = tf.keras.layers.Conv3D(1, 1, activation = 'relu', padding = 'same')(heatMap)

    group = tf.keras.layers.Conv3D(image_num_channels * 2, 3, activation = 'relu', padding = 'same')(inputs)
    group = tf.keras.layers.Conv3D(1, 1, activation = 'relu', padding = 'same')(group)

    regression = tf.keras.layers.Conv3D(image_num_channels * 2, 3, activation = 'relu', padding = 'same')(inputs)
    regression = tf.keras.layers.Conv3D(3, 1, activation = 'relu', padding = 'same')(regression)

    model = tf.keras.models.Model(inputs, [heatMap, group, regression])
    return model


def getCornerNetHead(image_spatial_dim, image_num_channels):

    TLF_cornerPooling = cornerPoolingModule(image_spatial_dim, image_num_channels, [TopPool, LeftPool, FrontPool])
    BRB_cornerPooling = cornerPoolingModule(image_spatial_dim, image_num_channels, [BottomPool, RightPool, BehindPool])

    TLF_prediction = predictionModule(image_spatial_dim, image_num_channels)
    BRB_prediction = predictionModule(image_spatial_dim, image_num_channels)

    inputs = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,))

    TLF = TLF_cornerPooling(inputs)
    TLF = TLF_prediction(TLF)

    BRB = BRB_cornerPooling(inputs)
    BRB = BRB_prediction(BRB)

    model = tf.keras.models.Model(inputs, [TLF, BRB])
    return model