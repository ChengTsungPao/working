import cv2
import math
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def getAngleMagnitude(Gradient):
    
    mag = []
    angle = []
    for Gx, Gy in Gradient:
        mag.append((Gx ** 2 + Gy ** 2) ** 0.5)
        val = np.angle(complex(Gx, Gy), deg=True)
        if val < 0:
            val += 360
        angle.append(val)
        # angle.append(np.angle(complex(Gx, Gy), deg=True))

    return np.array(mag), np.array(angle)

def getGradient(image, contour, imageType):
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    shape = np.shape(image)

    sobelx = cv2.Sobel(image,cv2.CV_64F, 1, 0, ksize=11)
    sobely = cv2.Sobel(image,cv2.CV_64F, 0, 1, ksize=11)

    newContour = []
    for x in contour:
        newContour.append(x[0])

    if imageType == "L":
        newContour.sort(key = lambda x: math.atan(abs(shape[0] - x[1]) / abs(shape[1] - x[0])))
    else:
        newContour.sort(key = lambda x: math.atan(abs(0 - x[1]) / abs(shape[1] - x[0])))

    Gradient = []
    for pos in newContour:
        y, x = pos[0], pos[1]
        Gx, Gy = sobelx[x][y], sobely[x][y]
        Gradient.append((restrictRange(Gx), restrictRange(Gy)))

    return Gradient, newContour

def restrictRange(val):
    return val
    # return max(min(abs(val), 255), 0)
