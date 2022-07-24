from create_model import get3DUnet, getDetectionHead
import tensorflow as tf


def get_data(path):
    pass

def train():
    IMAGE_SPATIAL_DIMS = (128, 128, 128)
    IMAGE_NUM_CHANNELS = 1
    NUM_CLASSES        = 2
    backbone_fpn_model = get3DUnet(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS, NUM_CLASSES)
    # detection_head = getDetectionHead(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)


if __name__ == "__main__":
    pass

