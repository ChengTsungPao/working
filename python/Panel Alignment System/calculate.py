import cv2, copy
import math
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def getAngleMagnitude(Gradient, imageType):
    
    mag = []
    angle = []
    for Gx, Gy in Gradient:
        mag.append((Gx ** 2 + Gy ** 2) ** 0.5)
        if imageType == "L":
            angle.append(np.angle(complex(Gx, Gy), deg=True))
        else:
            val = np.angle(complex(Gx, Gy), deg=True)
            if val < 0:
                val += 360
            angle.append(val)
        

    return np.array(mag), np.array(angle)

def transferContour(shape, contour, imageType):

    def angle_distance(pos, param):
        angle = math.atan(abs(param[0] - pos[1]) / abs(param[1] - pos[0]))
        distance = ((param[0] - pos[1]) ** 2 + (param[1] - pos[0]) ** 2) ** 0.5
        return angle, distance

    def contour_transfer(newContour, param):
        temp = [newContour[0]]
        for i in range(1, len(newContour)):
            angle1, distance1 = angle_distance(temp[-1], [param[0], param[1]])
            angle2, distance2 = angle_distance(newContour[i], [param[0], param[1]])
            if min(abs(angle1 - angle2), np.pi - abs(angle1 - angle2)) <= 0.05 * np.pi / 180:
                # print("remove {}".format(i))
                if abs(distance1 - distance2) >= 1:
                    if distance1 > distance2:
                        temp[-1] = copy.copy(newContour[i])
                    else:
                        pass
                else:
                    temp.append(copy.copy(newContour[i]))
            else:
                temp.append(copy.copy(newContour[i]))
        return copy.deepcopy(temp)

    newContour = []
    for x in contour:
        newContour.append(x[0])

    if imageType == "L":
        newContour.sort(key = lambda x: math.atan(abs(shape[0] - x[1]) / abs(shape[1] - x[0])))
        newContour = contour_transfer(newContour, [shape[0], shape[1]])

    else:
        newContour.sort(key = lambda x: math.atan(abs(0 - x[1]) / abs(shape[1] - x[0])))
        newContour = contour_transfer(newContour, [0, shape[1]])

    return newContour


def getGradient(image, newContour):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(image,cv2.CV_64F, 1, 0, ksize=11)
    sobely = cv2.Sobel(image,cv2.CV_64F, 0, 1, ksize=11)

    Gradient = []
    for pos in newContour:
        y, x = pos[0], pos[1]
        Gx, Gy = sobelx[x][y], sobely[x][y]
        Gradient.append((restrictRange(Gx), restrictRange(Gy)))

    return Gradient

def restrictRange(val):
    return val
    # return max(min(abs(val), 255), 0)
