import cv2
import copy
import numpy as np
from calculate import getAngleMagnitude, getGradient
from parameter import getParameter


def imageProcessing(image, light, imageType = "L"):

    ################################# cropImage and resize #################################
    image = cropImage(image, imageType)
    shape = np.shape(image)
    image = cv2.resize(image, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)
    cropResizeImage = copy.deepcopy(image)


    ######################### Filter (medianBlur or GaussianBlur) #########################
    # image = cv2.medianBlur(image, 3)
    # image = cv2.bilateralFilter(image, 5, 75, 75)
    image = cv2.GaussianBlur(image, (3, 3), 0)


    #################################### contrastImage #################################### 
    # contrastImage
    # image = contrastImage(image)


    ############################## threshold and Sobelfilter ##############################
    # threshold = cv2.threshold(image, getParameter(light, imageType), 255, cv2.THRESH_BINARY)
    # sobelImage = Sobelfilter(image)


    ###################################### contours ####################################### 
    canny = cv2.Canny(image, 70, 130)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour = contours[-1]
    drawContour = cv2.drawContours(image, contour, -1, (0, 255, 255), 1)


    ############################ calulate magnitude and angle ############################## 
    Gradient, contour = getGradient(cropResizeImage, contour, imageType)
    magnitude, angle = getAngleMagnitude(Gradient, imageType)

    # for i in range(len(contour)):
    #     print("Index:{}, x:{}, y:{}, angle:{}".format(i, contour[i][0], contour[i][1], angle[i]))


    # return {"image": (sobelImage, threshold[1], drawContour, cropResizeImage), "result": (Gradient, magnitude, angle, contour)}
    return {"image": (canny, drawContour, cropResizeImage), "result": (Gradient, magnitude, angle, contour)}


def cropImage(image, imageType):
    x = 0 if imageType == "L" else 200
    y = 0

    w = 1080
    h = 660

    return image[y : y + h , x : x + w]


def contrastImage(image):
    return image + (image - 125) * 1.5


def Sobelfilter(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)

    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)

    image_Sobel = cv2.addWeighted(x,0.5,y,0.5,0)

    return image_Sobel