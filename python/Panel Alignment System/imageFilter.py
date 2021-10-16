import cv2
import matplotlib.pylab as plt
import numpy as np
import math
import copy

import warnings
warnings.filterwarnings("ignore")

def findContour(path, filename):
    originImage = readImage(path, filename)
    image = copy.deepcopy(originImage)

    image = cropImage(image)
    shape = np.shape(image)

    image = cv2.resize(image, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)
    image = cv2.medianBlur(image, 3)
    # image = contrastImage(image)

    threshold = cv2.threshold(image, 155, 255, cv2.THRESH_BINARY)

    canny = cv2.Canny(image, 70, 130)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour = contours[-1]
    draw = cv2.drawContours(image.copy(), contour, -1, (0, 0, 255), 2)

    cv2.imshow("threshold", threshold[1])
    cv2.imshow("canny", canny)
    cv2.imshow("contour", draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    Gradient, data = getGradient(originImage, contour)
    mag, angle = getAngleMag(Gradient)

    plotResult(angle)

    index = 348
    drawImage(draw, data[index])

def readImage(path, filename):
    return cv2.imread(path + filename)

def cropImage(image):
    x = 0
    y = 0

    w = 1080
    h = 830

    return image[y : y + h , x : x + w]

def contrastImage(image):
    return image + (image - 125) * 1.5

def getGradient(image, contour):
    
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
    data.sort(key = lambda x: math.atan(abs(shape[0] - x[0]) / abs(shape[1] - x[1])))

    Gradient = []
    for pos in data:
        y, x = pos[0], pos[1]
        pixel = image[x - 1:x + 1 + 1:, y - 1:y + 1 + 1:]
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

def plotResult(result):
    
    plt.subplot(211)
    plt.title("result")
    plt.xlabel("index of point")
    plt.ylabel("degree")
    plt.plot(list(range(len(result))), result)
    
    plt.subplot(212)
    plt.title("dev result")
    plt.xlabel("index of point")
    plt.ylabel("degree")
    plt.plot(list(range(len(result) - 1)), np.abs(result[:-1] - result[1:]))
    plt.show()


def drawImage(draw, point):
    cv2.line(draw, (point[0], point[1]), (point[0], point[1]), (255, 0, 0), 5)
    cv2.imshow("result", draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
