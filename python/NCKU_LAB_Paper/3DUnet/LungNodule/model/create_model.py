import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import argparse
import tensorflow as tf

from backbone.Attention3DUnet import unets as attUnet
from backbone.Base3DUnet import unet as baseUnet
from head.RPNHead import rpn_head as rpn
from head.RPNHead.utils import create_anchor as anchor
from head.RPNHead.loss_function import rpn_loss
from head.CornerNetHead import cornerNet_head as cornerNet
from head.CornerNetHead.loss_function import cornerNetLoss

import warnings
warnings.filterwarnings('ignore', '.*output shape of zoom.*')


def get3DAttentionUnet(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, NUM_CLASSES):

    prsr = argparse.ArgumentParser(description='Command Line Arguments for Training Script')

    # U-Net Hyperparameters
    prsr.add_argument('--UNET_DENSE_SKIP',            type=int,   default=0,                                                                   help="U-Net: Enable Dense Skip Connections (Ref:UNet++)")
    prsr.add_argument('--UNET_DEEP_SUPERVISION',      type=int,   default=0,                                                                   help="U-Net: Enable Deep Supervision")
    prsr.add_argument('--UNET_PROBABILISTIC',         type=int,   default=0,                                                                   help="U-Net: Enable Probabilistic/Bayesian Output Computation")
    prsr.add_argument('--UNET_PROBA_LATENT_DIMS',     type=int,   default=[3,2,1,0],                                                nargs='+', help="U-Net: Probabilistic Latent Dimensions at Each Resolution")
    prsr.add_argument('--UNET_PROBA_ITER',            type=int,   default=1,                                                                   help="U-Net: Iterations of Probabilistic Inference During Validation")
    prsr.add_argument('--UNET_FEATURE_CHANNELS',      type=int,   default=[16,32,64,128,256],                                       nargs='+', help="U-Net: Encoder/Decoder Channels")
    prsr.add_argument('--UNET_STRIDES',               type=int,   default=[(1,1,1),(1,2,2),(1,2,2),(2,2,2),(2,2,2)],                nargs='+', help="U-Net: Down/Upsampling Factor per Resolution")
    prsr.add_argument('--UNET_KERNEL_SIZES',          type=int,   default=[(1,3,3),(1,3,3),(3,3,3),(3,3,3),(3,3,3)],                nargs='+', help="U-Net: Convolution Kernel Sizes")
    prsr.add_argument('--UNET_ATT_SUBSAMP',           type=int,   default=[(1,1,1),(1,1,1),(1,1,1),(1,1,1)],                        nargs='+', help="U-Net: Attention Gate Subsampling Factor")
    prsr.add_argument('--UNET_SE_REDUCTION',          type=int,   default=[8,8,8,8,8],                                              nargs='+', help="U-Net: Squeeze-and-Excitation Reduction Ratio")
    prsr.add_argument('--UNET_KERNEL_REGULARIZER_L2', type=float, default=1e-5,                                                                help="U-Net: L2 Kernel Regularizer (Contributes to Total Loss at Train-Time)")
    prsr.add_argument('--UNET_BIAS_REGULARIZER_L2',   type=float, default=1e-5,                                                                help="U-Net: L2 Bias Regularizer (Contributes to Total Loss at Train-Time)")
    prsr.add_argument('--UNET_DROPOUT_MODE',          type=str,   default="monte-carlo",                                                       help="U-Net: Dropout Mode: 'standard'/'monte-carlo'")
    prsr.add_argument('--UNET_DROPOUT_RATE',          type=float, default=0.50,                                                                help="U-Net: Dropout Regularization Rate")
    args, _ = prsr.parse_known_args()

    model = attUnet.networks.M1( input_spatial_dims = IMAGE_SPATIAL_DIMS,               
                                 input_channels     = IMAGE_NUM_CHANNELS,
                                 num_classes        = NUM_CLASSES,                      
                                 filters            = args.UNET_FEATURE_CHANNELS,                            
                                 dropout_rate       = args.UNET_DROPOUT_RATE,           
                                 strides            = args.UNET_STRIDES,
                                 kernel_sizes       = args.UNET_KERNEL_SIZES,           
                                 dropout_mode       = args.UNET_DROPOUT_MODE,
                                 se_reduction       = args.UNET_SE_REDUCTION,           
                                 att_sub_samp       = args.UNET_ATT_SUBSAMP,
                                 probabilistic      = bool(args.UNET_PROBABILISTIC),    
                                 prob_latent_dims   = args.UNET_PROBA_LATENT_DIMS,
                                 dense_skip         = bool(args.UNET_DENSE_SKIP),                                       
                                 deep_supervision   = bool(args.UNET_DEEP_SUPERVISION), 
                                 summary            = True,
                                 bias_initializer   = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.001),   
                                 bias_regularizer   = tf.keras.regularizers.l2(args.UNET_BIAS_REGULARIZER_L2),                                               
                                 kernel_initializer = tf.keras.initializers.Orthogonal(gain=1.0), 
                                 kernel_regularizer = tf.keras.regularizers.l2(args.UNET_KERNEL_REGULARIZER_L2)) 

    return model

# Unet + RPN
def getModel1(image_spatial_dim, image_num_channels):

    image_spatial_dim1, image_spatial_dim2 = image_spatial_dim
    image_num_channels1, image_num_channels2 = image_num_channels

    anchors = anchor.make_rpn_windows(image_spatial_dim2)

    def loss(reg, cls, targets):
        # worse running time
        return sum([rpn_loss(batch_reg, batch_cls, batch_targets, anchors) for batch_reg, batch_cls, batch_targets in zip(reg, cls, targets)])

    unet_model = baseUnet.get3DUnet(image_spatial_dim1, image_num_channels1)
    detection_head = rpn.getRPNHead(image_spatial_dim2, image_num_channels2)
    
    inputs = tf.keras.layers.Input(image_spatial_dim1 + (image_num_channels1,))

    x = unet_model(inputs)
    outputs = detection_head(x)

    model = tf.keras.models.Model(inputs, outputs)
    model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-4), loss = loss, metrics = [loss])
    return model

# Unet + CornerNet
def getModel2(image_spatial_dim, image_num_channels, model_path = None):

    image_spatial_dim1, image_spatial_dim2 = image_spatial_dim
    image_num_channels1, image_num_channels2 = image_num_channels
    scale = image_spatial_dim1[0] // image_spatial_dim2[0]

    # predicts: [TLF_heatMap, TLF_group, TLF_regression, BRB_heatMap, BRB_group, BRB_regression]  (TLF_heatMap also have many batch)
    # targets : [[[h0, w0, d0], [h1, w1, d1]...], [[h0, w0, d0], [h1, w1, d1]...] ....]
    def loss(targets, predicts):
        return cornerNetLoss(predicts, targets, scale)

    if model_path:
        model = tf.keras.models.load_model(model_path, custom_objects = {'loss': loss})
        model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-4), loss = loss)
        return model

    unet_model = baseUnet.get3DUnet(image_spatial_dim1, image_num_channels1, int(np.log2(scale) + 1))
    cornerNetHead = cornerNet.getCornerNetHead(image_spatial_dim2, image_num_channels2)

    inputs = tf.keras.layers.Input(image_spatial_dim1 + (image_num_channels1,))
    x = unet_model(inputs)
    outputs = cornerNetHead(x)

    model = tf.keras.models.Model(inputs, outputs)
    model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-4), loss = loss)
    return model

# Unet
def getModel3(image_spatial_dim, image_num_channels, model_path = None):

    def dice_coef_loss(y_true,y_pred,axis=(1,2,3),smooth=0.0001):
        intersection = tf.reduce_sum(y_true*y_pred,axis)
        total=tf.reduce_sum(tf.square(y_pred),axis)+tf.reduce_sum(tf.square(y_true),axis)
        numerator=tf.reduce_mean(intersection+smooth)
        denominator=tf.reduce_mean(total+smooth)
        dice_loss=-tf.math.log(2.*numerator)+tf.math.log(denominator)
        return dice_loss

    unet_model = baseUnet.get3DUnetSegm(image_spatial_dim, image_num_channels)

    inputs = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,))
    outputs = unet_model(inputs)

    model = tf.keras.models.Model(inputs, outputs)
    model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 1e-4), loss = dice_coef_loss)
    return model    


if __name__ == "__main__":

    physical_devices = tf.config.experimental.list_physical_devices("GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

    IMAGE_SPATIAL_DIMS = [(128, 128, 128), (128, 128, 128)]
    IMAGE_NUM_CHANNELS = [1, 1]

    image = np.ones((1,) + IMAGE_SPATIAL_DIMS[0] + (IMAGE_NUM_CHANNELS[0],))

    # model1 = getModel1(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)
    # cls, bbox = model1(image)
    # print(cls.shape)
    # print(bbox.shape)

    model2 = getModel2(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)
    outputs = model2(image)
    print("TLF => heatMap    : ", outputs[0].shape)
    print("TLF => group      : ", outputs[1].shape)
    print("TLF => regression : ", outputs[2].shape)
    print("BRB => heatMap    : ", outputs[3].shape)
    print("BRB => group      : ", outputs[4].shape)
    print("BRB => regression : ", outputs[5].shape)

    # model = get3DAttentionUnet(IMAGE_SPATIAL_DIMS[0], IMAGE_NUM_CHANNELS[0], 1)
    # print(model(image).shape)

