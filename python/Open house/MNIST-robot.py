import numpy as np
import tkinter as tk
import PIL.Image, PIL.ImageTk
import cv2

from keras.models import load_model
model = load_model('MNIST-robot.h5')

win_h, win_w = 600, 400

window = tk.Tk()
window.configure(background='wheat1')
window.title('Control panel')
window.geometry('{}x{}'.format(win_w,win_h))

img = np.zeros([800,800,3], np.uint8)
img_to_pred = np.zeros([800,800,3], np.uint8)

drawing = False
do_pred = False

R = 20
thickness = 100
kernalsize = 21
sigma = 500

def draw(event, x, y, flags,param):
    global drawing, ix ,iy, img, img_to_pred, do_pred
    color = (255,255,255)
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.line(img, (x,y), (x,y), color = color, thickness = thickness, lineType = cv2.LINE_AA)
        img_to_pred = cv2.resize(cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (kernalsize,kernalsize), sigma), (28,28) , interpolation = cv2.INTER_AREA)
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(img, (ix,iy), (x,y), color = color, thickness = thickness, lineType = cv2.LINE_AA)
            img_to_pred = cv2.resize(cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (kernalsize,kernalsize), sigma), (28,28) , interpolation = cv2.INTER_AREA)
            ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (ix,iy), (x,y), color = color ,  thickness = thickness, lineType = cv2.LINE_AA)
        img_to_pred = cv2.resize(cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (kernalsize,kernalsize), sigma), (28,28) , interpolation = cv2.INTER_AREA)
        do_pred = True
    return None

img = np.zeros([800,800,3], np.uint8)

cv2.namedWindow('Drawing window')
cv2.setMouseCallback('Drawing window', draw)

def refresh():
    global img, img_to_pred
    img = np.zeros([800,800,3], np.uint8)
    img_to_pred = np.zeros([800,800,3], np.uint8)
    label2.configure(text = 'Prediction : {}'.format('?'), font=('Agency FB Bold', 20))
    return None

def update_image():
    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
    img_in_tkinter = cv2.resize(img_to_pred,(300,300), interpolation = cv2.INTER_AREA)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img_in_tkinter))
    # Add a PhotoImage to the Canvas
    label.configure(image = photo)
    label.image = photo

    window.update_idletasks()
    window.update()

def close_window():
  global running
  running = False
  return None

title = tk.Label(window, text = '28x28 pixels', bg = 'green2', width = 20, font=('Agency FB Bold', 30))
title.grid(row = 0,padx = 40)

label = tk.Label(window)
label.grid(row = 1,padx = 40, pady = 10)

pre_number = '?'
label2 = tk.Label(window, text = 'Prediction : {}'.format(pre_number),width = 15, bg = 'pink2' ,font=('Agency FB Bold', 20))
label2.grid(row = 2,padx = 20, pady = 10)

refresh_button = tk.Button(window, text = 'Refresh', bg = 'cornflower blue' ,width = 10, height = 1, command = refresh, font=('Agency FB Bold', 20))
refresh_button.grid(row = 3,pady=10)

quit_button = tk.Button(window, text = 'Quit', bg = 'tomato' ,width = 10, height = 1, command = close_window, font=('Agency FB Bold', 20))
quit_button.grid(row = 4,pady=10)


window.protocol("WM_DELETE_WINDOW", close_window)
running = True

while running:
    update_image()
    cv2.imshow('Drawing window',img)

    if do_pred:
        feed_in_model = (img_to_pred.reshape(1, 28, 28, 1)/255.)
        prediction = model.predict_classes(feed_in_model)
        label2.configure(text = 'Prediction : {}'.format(prediction[0]), font=('Agency FB Bold', 20))
        do_pred = False
