import tensorflow as tf

def modelPrediction2(TLF, BRB, threshold = 0.8):    

    TLF_heatMap, TLF_group, TLF_regression = TLF
    BRB_heatMap, BRB_group, BRB_regression = BRB

    tlf_points = []
    for tlf in TLF_heatMap:
        tlf = tf.exp(tlf) / tf.reduce_sum(tf.exp(tlf), axis = tlf.shape, keepdims=True)
        tlf_points.append(tf.where(tlf > threshold).numpy())
    
    brb_points = []
    for brb in BRB_heatMap:
        brb = tf.exp(brb) / tf.reduce_sum(tf.exp(brb), axis = brb.shape, keepdims=True)
        brb_points.append(tf.where(brb > threshold).numpy())

    return tlf_points, brb_points