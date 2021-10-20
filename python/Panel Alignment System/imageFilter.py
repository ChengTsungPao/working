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
    tmp = copy.deepcopy(image)
    image = cv2.medianBlur(image, 3)
    # image = cv2.bilateralFilter(image, 5, 75, 75)
    # image = cv2.GaussianBlur(image, (5, 5), 0)
    # image = contrastImage(image)

    threshold = cv2.threshold(image, getParameter(light), 255, cv2.THRESH_BINARY)

    sobelImage = Sobelfilter(threshold[1])

    canny = cv2.Canny(threshold[1], 70, 130)
    contours, hierarchy = cv2.findContours(sobelImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour = contours[-1]
    # draw = cv2.drawContours(image.copy(), contour, -1, (0, 0, 255), 1)
    draw = cv2.drawContours(sobelImage.copy(), contour, -1, (0, 0, 255), 2)


    # tmp = diff(image, contour, imageType)
    # plt.plot(range(len(tmp)),tmp)
    # plt.show()

    cv2.imshow("sobelfilter", sobelImage)
    cv2.imshow("threshold", threshold[1])
    cv2.imshow("canny", canny)
    cv2.imshow("contour", draw)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    Gradient, data = getGradient(tmp, contour, imageType)
    mag, angle = getAngleMag(Gradient)


    plt.plot(list(range(len(Gradient))), Gradient, "-o")
    plt.show()

    plotAngle(path, filename, angle)

    index = 425
    # index = int(input("index = "))
    drawImage(path, filename, tmp, data[index])

def diff(image, contour, imageType):
    data = []
    for x in contour:
        data.append(x[0])

    shape = np.shape(image)
    if imageType == "L":
        data.sort(key = lambda x: math.atan(abs(shape[0] - x[1]) / abs(shape[1] - x[0])))
    else:
        data.sort(key = lambda x: math.atan(abs(0 - x[1]) / abs(shape[1] - x[0])))

    angle = []
    for i in range(1, len(data)):
        prePos, pos = data[i - 1], data[i]
        # data.append((pos[0] - prePos[0], pos[1] - prePos[1]))
        angle.append(math.atan((pos[1] - prePos[1]) / (pos[0] - prePos[0])) * 180 / np.pi)

    return angle


        

def readImage(path, filename):
    return cv2.imread(path + filename)

def Sobelfilter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    image_Sobel = cv2.addWeighted(x,0.5,y,0.5,0)
    return image_Sobel

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

    sobelx = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=11)
    sobely = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=11)

    data = []
    for x in contour:
        data.append(x[0])

    if imageType == "L":
        data.sort(key = lambda x: math.atan(abs(shape[0] - x[1]) / abs(shape[1] - x[0])))
    else:
        data.sort(key = lambda x: math.atan(abs(0 - x[1]) / abs(shape[1] - x[0])))
    # plt.imshow(sobelx)
    # plt.show()
    Gradient = []
    for pos in data:
        y, x = pos[0], pos[1]
        # print(image[x:][y])
        # image[x][y] = 500
        # plt.imshow(image)
        # plt.show()
        # Gx, Gy = 0, 0
        # for i in np.arange(-10, 11, 1):
        #     for j in np.arange(-10, 11, 1):
        #         Gx += sobelx[x][y]
        #         Gy += sobely[x][y]
        Gx, Gy = sobelx[x][y], sobely[x][y]
        # pixel = image[x - 1:x + 1 + 1:, y - 1:y + 1 + 1:]
        # if np.shape(pixel) == (3, 3):
        #     Gx = np.sum(pixel * Sx)
        #     Gy = np.sum(pixel * Sy)
        #     Gradient.append((restrictRange(Gx), restrictRange(Gy)))

        Gradient.append((restrictRange(Gx), restrictRange(Gy)))
    return Gradient, data


def restrictRange(val):
    return val
    # return max(min(abs(val), 255), 0)


def getAngleMag(Gradient):

    mag = []
    angle = []
    for Gx, Gy in Gradient:
        mag.append((Gx ** 2 + Gy ** 2) ** 0.5)
        val = math.atan(Gy / Gx) * 180 / np.pi
        if val < 0 and abs(val) > 45:
            val += 180
        angle.append(val)

    return np.array(mag), np.array(angle)

def plotAngle(path, filename, angle):
    
    # plt.subplot(211)
    plt.title("angle")
    plt.xlabel("index of point")
    plt.ylabel("degree")
    plt.plot(list(range(len(angle))), angle)
    
    # plt.subplot(212)
    # plt.title("dev angle")
    # plt.xlabel("index of point")
    # plt.ylabel("degree")
    # plt.plot(list(range(len(angle) - 1)), np.abs(angle[:-1] - angle[1:]))
    # plt.savefig(path + filename.split(".png")[0] + "_angle.png", dpi = 300)
    plt.show()


def drawImage(path, filename, draw, point):
    cv2.line(draw, (point[0], point[1]), (point[0], point[1]), (255, 0, 0), 5)
    cv2.imshow("result", draw)
    # cv2.imwrite(path + filename.split(".png")[0] + "_result.png", draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
