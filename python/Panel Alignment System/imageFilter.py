import cv2
import matplotlib.pylab as plt

def findContour(path, filename):
    image = readImage(path, filename)
    # cv2.imshow("Origin Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray Image", gray)

    # blurred = cv2.medianBlur(gray, 3)
    blurred = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    # cv2.imshow("medianBlur Image", blurred)

    canny = cv2.Canny(blurred, 125, 155)
    print(canny[500][500])
    
    cv2.imshow("canny Image", canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def readImage(path, filename):
    return cv2.imread(path + filename)