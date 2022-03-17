from Detect_Shot_Change import detect_shot_change
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

    thresholds = [
        750,
        1400,
        7400
    ]

    index = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('--imagePath', type = str, default = imagePaths[index], help = 'path of image')
    parser.add_argument('--groundTruthFile', type = str, default = groundTruthFiles[index], help = 'file of groundTruth')
    parser.add_argument('--threshold', type = int, default = thresholds[index], help = 'width of color histogram')
    parser.add_argument('--windowSize', type = int, default = 8, help = 'width of color histogram')
    args = parser.parse_args()

    shot_change_detection_fcn = detect_shot_change(args)
    # shot_change_detection_fcn.getColorShotChangeFrame()
    # shot_change_detection_fcn.getKeypointShotChangeFrame()
    shot_change_detection_fcn.getFourierShotChangeFrame()