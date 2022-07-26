from model.create_model import getModel
import tensorflow as tf


def get_data(path):
    pass

def train():
    IMAGE_SPATIAL_DIMS = [(512, 512, 32), (512, 512, 32)]
    IMAGE_NUM_CHANNELS = [1, 1]

    model = getModel(IMAGE_SPATIAL_DIMS, IMAGE_NUM_CHANNELS)



if __name__ == "__main__":
    pass

