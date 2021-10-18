import cv2
import matplotlib.pylab as plt
import numpy as np
import math
import copy

import warnings
warnings.filterwarnings("ignore")

def getParameter(light):
    
    table = {
        "light": "Binary",
            30 :  35 ,
            50 :  80 ,
           100 : 110 ,
           150 : 155 ,
           200 : 200 ,
           255 : 245
    }

    return table[light] 


def findContour(path, filename, light, imageType = "L"):
    originImage = readImage(path, filename)
    image = copy.deepcopy(originImage)

    image = cropImage(image, imageType)
    shape = np.shape(image)

    image = cv2.resize(image, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)
    image = cv2.medianBlur(image, 3)
    # image = contrastImage(image)

    threshold = cv2.threshold(image, getParameter(light), 255, cv2.THRESH_BINARY)

    canny = cv2.Canny(threshold[1], 70, 130)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour = contours[-1]
    draw = cv2.drawContours(image.copy(), contour, -1, (0, 0, 255), 2)

    # cv2.imshow("threshold", threshold[1])
    # cv2.imshow("canny", canny)
    # cv2.imshow("contour", draw)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    Gradient, data = getGradient(originImage, contour, imageType)
    mag, angle = getAngleMag(Gradient)

    plotResult(path, filename, angle)

    # index = 288
    index = int(input("index = "))
    drawImage(path, filename, draw, data[index])

def readImage(path, filename):
    return cv2.imread(path + filename)

def cropImage(image, imageType):
    x = 0 if imageType == "L" else 200
    y = 0

    w = 1080
    h = 830

    return image[y : y + h , x : x + w]

def contrastImage(image):
    return image + (image - 125) * 1.5

def getGradient(image, contour, imageType):
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    Sx = [
        [-2,  0,  2],
        [-1,  0,  1],
        [-2,  0,  2]
    ]

    Sy = [
        [-2, -1, -2],
        [ 0,  0,  0],
        [ 2,  1,  2]
    ]

    Sx = np.array(Sx)
    Sy = np.array(Sy)
    shape = np.shape(image)

    data = []
    for x in contour:
        data.append(x[0])

    if imageType == "L":
        data.sort(key = lambda x: math.atan(abs(shape[0] - x[1]) / abs(shape[1] - x[0])))
    else:
        data.sort(key = lambda x: math.atan(abs(0 - x[1]) / abs(shape[1] - x[0])))

    Gradient = []
    for pos in data:
        y, x = pos[0], pos[1]
        pixel = image[x - 1:x + 1 + 1:, y - 1:y + 1 + 1:]
        if np.shape(pixel) == (3, 3):
            Gx = np.sum(pixel * Sx)
            Gy = np.sum(pixel * Sy)
            Gradient.append((restrictRange(Gx), restrictRange(Gy)))

    return Gradient, data


def restrictRange(val):
    return max(min(abs(val), 255), 0)


def getAngleMag(Gradient):

    mag = []
    angle = []
    for Gx, Gy in Gradient:
        mag.append((Gx ** 2 + Gy ** 2) ** 0.5)
        angle.append(math.atan(Gy / Gx) * 180 / np.pi)

    return np.array(mag), np.array(angle)

def plotResult(path, filename, result):
    
    # plt.subplot(211)
    # plt.title("angle")
    # plt.xlabel("index of point")
    # plt.ylabel("degree")
    # plt.plot(list(range(len(result))), result)
    
    # plt.subplot(212)
    plt.title("dev angle")
    plt.xlabel("index of point")
    plt.ylabel("degree")
    plt.plot(list(range(len(result) - 1)), np.abs(result[:-1] - result[1:]))
    plt.savefig(path + filename.split(".png")[0] + "_angle.png", dpi = 300)
    plt.show()


def drawImage(path, filename, draw, point):
    cv2.line(draw, (point[0], point[1]), (point[0], point[1]), (255, 0, 0), 5)
    cv2.imshow("result", draw)
    cv2.imwrite(path + filename.split(".png")[0] + "_result.png", draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
