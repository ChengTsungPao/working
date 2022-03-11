from Shot_Change_Detection import shot_change_detection
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

    index = 0

    parser = argparse.ArgumentParser()
    parser.add_argument('--imagePath', type = str, default = imagePaths[index], help = 'path of image')
    parser.add_argument('--groundTruthFile', type = str, default = groundTruthFiles[index], help = 'file of groundTruth')
    parser.add_argument('--windowSize', type = int, default = 8, help = 'width of color histogram')
    args = parser.parse_args()

    shot_change_detection_fcn = shot_change_detection(args)
    shot_change_detection_fcn.getShotChangeFrame()