import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

    # from imageProcessing import imageProcessing
    # from plot import plotResult, drawImage
    # from glob import glob
    # import matplotlib.pylab as plt
    # import numpy as np
    # import os
    # import cv2

    # paths = glob("./Test Image_20210913/M3mm*")
    # # paths = ["./Test Image_20210913\\M3mm_Deg2.5_Bri150"]
    # for path in paths:
    #     light = int(path.split("Bri")[-1])
    #     path += "//"
    #     files = os.listdir(path)
    #     files = glob(path + "cal_*_L.png") + glob(path + "cal_*_R.png")
    #     for file_ in files:
    #         print(file_)