import cv2
import matplotlib.pylab as plt
import numpy as np

def readImage(path, filename):
    return cv2.imread(path + filename)

def cropImage(image):
    # 裁切區域的 x 與 y 座標（左上角）
    x = 0
    y = 0

    # 裁切區域的長度與寬度
    w = 1080
    h = 830

    # 裁切圖片
    return image[y : y + h , x : x + w]

def contrastImage(image):
    ######################################
    alpha = 1.5
    # 255 + (255 - 125) * 1.5 > 255
    # contpre = image + (image - 0) * alpha
    ######################################

    array_alpha = np.array([1.5]) # contrast 
    array_beta = np.array([0.0]) # brightness
    print(image)
    # add a beta value to every pixel 
    image = cv2.add(image, array_beta)                    

    # multiply every pixel value by alpha
    image = cv2.multiply(image, array_alpha)

    # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
    image = np.clip(image, 0, 255)
    print("=================================")
    print(image)

    return image + (image - 125) * alpha

def findContour(path, filename):
    image = readImage(path, filename)

    image = cropImage(image)
    shape = np.shape(image)

    image = cv2.resize(image, (shape[1] // 2, shape[0] // 2), interpolation=cv2.INTER_AREA)
    image = cv2.medianBlur(image, 3)
    # image = contrastImage(image)

    threshold = cv2.threshold(image, 155, 255, cv2.THRESH_BINARY)
    cv2.imshow("out threshold", threshold[1])

    canny = cv2.Canny(image, 70, 130)
    cv2.imshow("out canny", canny)

    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    draw_img0 = cv2.drawContours(image.copy(), contours, -1, (0, 0, 255), 2)
    cv2.imshow("contours", draw_img0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)