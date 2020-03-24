import cv2
import numpy as np
import matplotlib.pyplot as plt
def Sobelfilter(gray):
    sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
    image_Sobel = np.uint8(np.absolute(sobely))
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    image_Sobel = cv2.addWeighted(x,0.5,y,0.5,0)
    return image_Sobel

def Cannyedge(gray,visible=False):
    lowThreshold = 10
    max_lowThreshold = 10#40
    edges = cv2.Canny(gray, lowThreshold, max_lowThreshold)
    if(visible):
        cv2.imshow('detected circles',edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return edges