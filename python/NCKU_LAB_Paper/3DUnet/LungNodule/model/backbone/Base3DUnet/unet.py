import tensorflow as tf

def get3DUnet(image_spatial_dim, image_num_channels, downResolution = 1):
    
    downResolution = downResolution if 0 < downResolution <= 4 else 1

    inputs = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,))
    conv1 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same',data_format="channels_last")(inputs)

    conv1 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same')(conv1)
    pool1 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(conv1)
    conv2 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same')(pool1)

    conv2 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same')(conv2)
    pool2 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(conv2)
    conv3 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same')(pool2)

    conv3 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same')(conv3)
    pool3 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(conv3)
    conv4 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same')(pool3)

    conv4 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same')(conv4)
    drop4 = tf.keras.layers.Dropout(0.5)(conv4)
    pool4 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(drop4)

    conv5 = tf.keras.layers.Conv3D(128, 3, activation = 'relu', padding = 'same')(pool4)
    conv5 = tf.keras.layers.Conv3D(128, 3, activation = 'relu', padding = 'same')(conv5)
    drop5 = tf.keras.layers.Dropout(0.5)(conv5)

    if downResolution <= 4:
        up6 = tf.keras.layers.Conv3D(64, 2, activation = 'relu', padding = 'same')(tf.keras.layers.UpSampling3D(size = (2,2,2))(drop5))
        merge6 = tf.keras.layers.concatenate([drop4,up6],axis=-1)
        conv6 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same')(merge6)
        conv6 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same')(conv6)
        outputs = conv6

    if downResolution <= 3:
        up7 = tf.keras.layers.Conv3D(32, 2, activation = 'relu', padding = 'same')(tf.keras.layers.UpSampling3D(size = (2,2,2))(conv6))
        merge7 = tf.keras.layers.concatenate([conv3,up7],axis=-1)
        conv7 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same')(merge7)
        conv7 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same')(conv7)
        outputs = conv7

    if downResolution <= 2:
        up8 = tf.keras.layers.Conv3D(16, 2, activation = 'relu', padding = 'same')(tf.keras.layers.UpSampling3D(size = (2,2,2))(conv7))
        merge8 = tf.keras.layers.concatenate([conv2,up8],axis=-1)
        conv8 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same')(merge8)
        conv8 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same')(conv8)
        outputs = conv8

    if downResolution <= 1:
        up9 = tf.keras.layers.Conv3D(8, 2, activation = 'relu', padding = 'same')(tf.keras.layers.UpSampling3D(size = (2,2,2))(conv8))
        merge9 = tf.keras.layers.concatenate([conv1,up9],axis=-1)
        conv9 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same')(merge9)
        conv9 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same')(conv9)
        outputs = conv9
    
    # sigmoid or not ???
    outputs = tf.keras.layers.Conv3D(1, 1)(outputs)
    model = tf.keras.models.Model(inputs, outputs)

    return model


def get3DUnetSegm(image_spatial_dim, image_num_channels):

    inputs = tf.keras.layers.Input(image_spatial_dim + (image_num_channels,), name='brats_mr_image') # (512, 512, 7, 1)

    conv1 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
    conv1 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
    # LN1=tfa.layers.InstanceNormalization()(conv1)
    LN1 = tf.keras.layers.BatchNormalization()(conv1)
    pool1 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(LN1)
    conv2 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
    conv2 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
    # LN2=tfa.layers.InstanceNormalization()(conv2)
    LN2 = tf.keras.layers.BatchNormalization()(conv2)
    pool2 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(LN2)
    conv3 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
    conv3 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
    # LN3=tfa.layers.InstanceNormalization()(conv3)
    LN3 = tf.keras.layers.BatchNormalization()(conv3)
    pool3 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(LN3)
    conv4 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
    conv4 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
    # LN4=tfa.layers.InstanceNormalization()(conv4)
    LN4 = tf.keras.layers.BatchNormalization()(conv4)
    #drop4 = tf.keras.layers.Dropout(0.5)(LN4)
	
    #pool4 = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 1))(LN4)

    #conv5 = tf.keras.layers.Conv3D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    #conv5 = tf.keras.layers.Conv3D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
	
    #drop5 = tf.keras.layers.Dropout(0.5)(conv5)

    #up6 = tf.keras.layers.Conv3D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(tf.keras.layers.UpSampling3D(size = (2,2,1))(conv5))
    #merge6 = tf.keras.layers.concatenate([conv4,up6],axis=-1)
    conv6 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(LN4)
    conv6 = tf.keras.layers.Conv3D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)

    up7 = tf.keras.layers.Conv3D(32, 2, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(tf.keras.layers.UpSampling3D(size = (2,2,2))(conv6))
    merge7 = tf.keras.layers.concatenate([conv3,up7],axis=-1)
    conv7 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(merge7)
    conv7 = tf.keras.layers.Conv3D(32, 3, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(conv7)
	
	
    up8 = tf.keras.layers.Conv3D(16, 2, activation = 'relu', padding = 'same')(tf.keras.layers.UpSampling3D(size = (2,2,2))(conv7))
    merge8 = tf.keras.layers.concatenate([conv2,up8],axis=-1)
    conv8 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(merge8)
    conv8 = tf.keras.layers.Conv3D(16, 3, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(conv8)
	
	
    up9 = tf.keras.layers.Conv3D(8, 2, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(tf.keras.layers.UpSampling3D(size = (2,2,2))(conv8))
    merge9 = tf.keras.layers.concatenate([conv1,up9],axis=-1)
    conv9 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(merge9)
    conv9 = tf.keras.layers.Conv3D(8, 3, activation = 'relu', padding = 'same' ,kernel_initializer = 'he_normal')(conv9)
    conv10 = tf.keras.layers.Conv3D(1, 1, activation = 'sigmoid')(conv9)

    model = tf.keras.models.Model(inputs=[inputs], outputs=conv10)

    return model