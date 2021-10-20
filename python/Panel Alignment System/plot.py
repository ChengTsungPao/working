import matplotlib.pylab as plt
import cv2

def plotResult(title, xlabel, ylabel, result):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(range(len(result)), result)

def drawImage(draw, title, point = []):
    if point != []:
        cv2.line(draw, (point[0], point[1]), (point[0], point[1]), (255, 0, 0), 5)
    cv2.imshow(title, draw)