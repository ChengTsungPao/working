from imageProcessing import imageProcessing
from plot import plotResult, drawImage
from glob import glob
import matplotlib.pylab as plt
import os
import cv2

if __name__ == "__main__":
    # paths = glob("./Test Image_20210913/M3mm*")
    # paths = ["./Test Image_20210913\\M3mm_Deg2.5_Bri150"]
    # for path in paths:
    #     light = int(path.split("Bri")[-1])
    #     path += "//"
    #     files = os.listdir(path)
    #     for filename in files:
    #         if filename.split(".png")[0][-1] == "L":
    #             imageProcessing(image, light, imageType, False)
    #             findContour(path, filename, light, filename.split(".png")[0][-1])
    
    index = 5

    light = 100
    degree = 2.5
    imageType = "L"

    path = "./Test Image_20210913/M3mm_Deg{}_Bri{}/".format(str(degree), str(light))
    filename = "cal_{}_{}.png".format(str(index), imageType)


    image = cv2.imread(path + filename)
    data = imageProcessing(image, light, imageType)
    sobelImage, threshold, drawContour = data["image"]
    Gradient, magnitude, angle, contour = data["result"]
    drawImage(sobelImage, "sobelfilter")
    drawImage(threshold, "threshold")
    drawImage(drawContour, "contour")
    drawImage(drawContour, "result", contour[425])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    plt.subplot(221)
    plotResult("Gradient", "index of point", "G", Gradient)
    plt.subplot(223)
    plotResult("magnitude", "index of point", "degree", magnitude)
    plt.subplot(224)
    plotResult("Angle", "index of point", "degree", angle)
    plt.show()
    