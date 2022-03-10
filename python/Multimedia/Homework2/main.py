from Shot_Change_Detection import shot_change_detection

if __name__ == "__main__":
    
    imagePath = "./dataset/hw2_1/news_out/"
    groundTruthFile = "./dataset/hw2_1/news_ground.txt"

    # imagePath = "./dataset/hw2_1/ngc_out/"
    # groundTruthFile = "./dataset/hw2_1/ngc_ground.txt"

    # imagePath = "./dataset/hw2_2/ftfm_out/"
    # groundTruthFile = "./dataset/hw2_2/ftfm_ground.txt"

    shot_change_detection_fcn = shot_change_detection(imagePath, groundTruthFile)
    shot_change_detection_fcn.color_histogram()