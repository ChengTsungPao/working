from Detect_Shot_Change import detect_shot_change
import matplotlib.pylab as plt
import numpy as np
import argparse


if __name__ == "__main__":

    imagePaths = [
        "./dataset/hw2_1/news_out/",
        "./dataset/hw2_1/ngc_out/",
        "./dataset/hw2_2/ftfm_out/"
    ]

    groundTruthFiles = [
        "./dataset/hw2_1/news_ground.txt",
        "./dataset/hw2_1/ngc_ground.txt",
        "./dataset/hw2_2/ftfm_ground.txt"
    ]

    algorithm = "color_histogram1"
    videoIndex = 2

    precisions, recalls, FSRs = [], [], []

    for threshold in np.arange(0.1, 1.1, 0.01):

        parser = argparse.ArgumentParser()
        parser.add_argument('--imagePath', type = str, default = imagePaths[videoIndex], help = 'path of image')
        parser.add_argument('--groundTruthFile', type = str, default = groundTruthFiles[videoIndex], help = 'file of groundTruth')
        parser.add_argument('--algorithm', type = str, default = algorithm, help = 'algorithm of function')
        parser.add_argument('--threshold', type = int, default = threshold, help = 'width of color histogram')
        parser.add_argument('--windowSize', type = int, default = 8, help = 'width of color histogram')
        args = parser.parse_args()

        shot_change_detection_fcn = detect_shot_change(args)
        precision, recall, FSR = shot_change_detection_fcn.getShotChangeFrame()

        precisions.append(precision)
        recalls.append(recall)
        FSRs.append(FSR)

    np.savez("./dataset/Result/video{}_{}.npz".format(videoIndex, algorithm), precision = precisions, recall = recalls, FSR = FSRs)

    result = np.load("./dataset/Result/video{}_{}.npz".format(videoIndex, algorithm))

    plt.clf()
    plt.plot(result["recall"], result["precision"], "-o")
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.show()

    plt.clf()
    plt.plot(result["FSR"], result["recall"], "-o")
    plt.xlabel("FSR")
    plt.ylabel("recall")
    plt.show()



