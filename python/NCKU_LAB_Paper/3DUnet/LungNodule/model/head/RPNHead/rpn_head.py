from .utils.create_anchor import get_anchors
import tensorflow as tf
import numpy as np

def getRPNHead(image_spatial_dim, image_num_channels):
    
    anchor_num = len(get_anchors())

    inputs = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,))
    cls_layer = tf.keras.layers.Conv3D(anchor_num * 2, 3, padding = 'same')(inputs)
    cls_layer = tf.keras.layers.Reshape((np.prod(cls_layer.shape[1: -1]) * anchor_num, 2))(cls_layer)
    cls_layer = tf.keras.layers.Softmax(axis = -1)(cls_layer)
    reg_layer = tf.keras.layers.Conv3D(anchor_num * 6, 3, padding = 'same')(inputs)
    reg_layer = tf.keras.layers.Reshape((np.prod(reg_layer.shape[1: -1]) * anchor_num, 6))(reg_layer)

    model = tf.keras.models.Model(inputs, [cls_layer, reg_layer])
    return model