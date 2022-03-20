from Detect_Shot_Change import detect_shot_change
import matplotlib.pylab as plt
import numpy as np
import argparse
import os

def calculate(algorithm, videoIndex, args):
    start_threshold = [0.65, 0.45, 0.6]
    precisions, recalls, FSRs = [], [], []

    for threshold in np.arange(start_threshold[videoIndex], 1.1, 0.05):
        args.threshold = threshold

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
    plt.savefig("./dataset/Result/video{}_{}_1.png".format(videoIndex, algorithm))

    plt.clf()
    plt.plot(result["FSR"], result["recall"], "-o")
    plt.xlabel("FSR")
    plt.ylabel("recall")
    plt.savefig("./dataset/Result/video{}_{}_2.png".format(videoIndex, algorithm))


def plot(algorithm):
    titlefont = 20
    font = 15
    video = ["news_out", "ngc_out", "ftfm_out"]

    plt.clf()
    plt.title("PR-Curve", fontsize=titlefont)
    for videoIndex in range(3):
        result = np.load("./dataset/Result/video{}_{}.npz".format(videoIndex, algorithm))
        plt.plot(result["recall"], result["precision"], "-o", label = video[videoIndex])

    plt.xlabel("recall", fontsize=font)
    plt.ylabel("precision", fontsize=font)
    plt.legend()
    plt.savefig("./dataset/Result/precision_recall_{}.png".format(algorithm))
    plt.show()

    plt.clf()
    plt.title("RF Curve", fontsize=titlefont)
    for videoIndex in range(3):
        result = np.load("./dataset/Result/video{}_{}.npz".format(videoIndex, algorithm))
        plt.plot(result["FSR"], result["recall"], "-o", label = video[videoIndex])

    plt.xlabel("FSR", fontsize=font)
    plt.ylabel("recall", fontsize=font)
    plt.legend()
    plt.savefig("./dataset/Result/recall_FSR_{}.png".format(algorithm))
    plt.show()



if __name__ == "__main__":
    if not os.path.exists("./dataset/Result/"):
        os.makedirs("./dataset/Result/")

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

    for videoIndex in range(3):
        parser = argparse.ArgumentParser()
        parser.add_argument('--imagePath', type = str, default = imagePaths[videoIndex], help = 'path of image')
        parser.add_argument('--groundTruthFile', type = str, default = groundTruthFiles[videoIndex], help = 'file of groundTruth')
        parser.add_argument('--algorithm', type = str, default = algorithm, help = 'algorithm of function')
        parser.add_argument('--threshold', type = int, default = 0.85, help = 'width of color histogram')
        parser.add_argument('--windowSize', type = int, default = 8, help = 'width of color histogram')
        args = parser.parse_args()
        calculate(algorithm, videoIndex, args)
        print("Video{} Finish !!!".format(videoIndex))

    plot(algorithm)
