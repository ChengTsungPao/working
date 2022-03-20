from Detect_Shot_Change import detect_shot_change
import argparse
import os

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

    thresholds = {
         "color_histogram1": [ 0.90,  0.95,  0.85],
         "color_histogram2": [ -750, -1400, -7500],
        "keypoints_dection": [    0,     0,     0],
        "fourier_transform": [    0,     0,     0]
    }

    algorithm = "color_histogram1"
    videoIndex = 2

    parser = argparse.ArgumentParser()
    parser.add_argument('--imagePath', type = str, default = imagePaths[videoIndex], help = 'path of image')
    parser.add_argument('--groundTruthFile', type = str, default = groundTruthFiles[videoIndex], help = 'file of groundTruth')
    parser.add_argument('--algorithm', type = str, default = algorithm, help = 'algorithm of function')
    parser.add_argument('--threshold', type = int, default = thresholds[algorithm][videoIndex], help = 'width of color histogram')
    parser.add_argument('--windowSize', type = int, default = 8, help = 'width of color histogram')
    args = parser.parse_args()

    shot_change_detection_fcn = detect_shot_change(args)
    shot_change_detection_fcn.getShotChangeFrame()
