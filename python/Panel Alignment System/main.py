from imageFilter import findContour
from glob import glob
import os

if __name__ == "__main__":
    # paths = glob("./Test Image_20210913/M3mm*")
    # paths = ["./Test Image_20210913\\M3mm_Deg2.5_Bri150"]
    # for path in paths:
    #     light = int(path.split("Bri")[-1])
    #     path += "//"
    #     files = os.listdir(path)
    #     for filename in files:
    #         if filename.split(".png")[0][-1] == "L":
    #             findContour(path, filename, light, filename.split(".png")[0][-1])
    
    path = "./Test Image_20210913/M3mm_Deg2.5_Bri200/"
    filename = "cal_8_R.png"
    light = 200
    findContour(path, filename, light)
    