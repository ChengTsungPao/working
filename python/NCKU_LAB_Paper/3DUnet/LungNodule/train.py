from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import numpy as np
import argparse
import tensorflow as tf
import model.unets as unets
                      
import warnings
warnings.filterwarnings('ignore', '.*output shape of zoom.*')

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

IMAGE_SPATIAL_DIMS = (128, 128, 128)
IMAGE_NUM_CHANNELS = 1
NUM_CLASSES        = 1
SHOW_SUMMARY = True

unet_model = unets.networks.M1( input_spatial_dims = IMAGE_SPATIAL_DIMS,               
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
                                summary            = SHOW_SUMMARY,
                                bias_initializer   = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.001),   
                                bias_regularizer   = tf.keras.regularizers.l2(args.UNET_BIAS_REGULARIZER_L2),                                               
                                kernel_initializer = tf.keras.initializers.Orthogonal(gain=1.0), 
                                kernel_regularizer = tf.keras.regularizers.l2(args.UNET_KERNEL_REGULARIZER_L2)) 


if __name__ == "__main__":
    image = np.ones((1,) + IMAGE_SPATIAL_DIMS + (IMAGE_NUM_CHANNELS,))
    output = unet_model(image)
    print(output.shape)

