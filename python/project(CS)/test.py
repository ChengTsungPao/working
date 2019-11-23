import cv2
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
#import copy

#filename = "test1.bmp"
filename = "test2.bmp"
#filename = "test3.bmp"
#filename = "Height 091203.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/"

lowThreshold = 3
max_lowThreshold = 40
kernel_size = 3
 
#img = cv2.imread("Height2.bmp")
img = cv2.imread(path+filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
'''

blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), cv2.BORDER_DEFAULT)
edges = cv2.Canny(blur_gray, lowThreshold, max_lowThreshold)
plt.imshow(edges, cmap='Greys_r')

plt.show()

'''
#img = cv2.medianBlur(edges,5)
#img = gray
minr , maxr = 70 , 150
#minr , maxr = 0 , 700 
#minr , maxr = 390 , 430 
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=minr,maxRadius=maxr)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:  
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle

cv2.imshow('detected circles',img)
cv2.waitKey(0)
cv2.destroyAllWindows()