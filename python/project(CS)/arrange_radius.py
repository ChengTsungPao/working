import cv2
from arrange import HighCircle,take_line,Radiuscal
from filters import Sobelfilter
import numpy as np

flag = True
while(flag):
    choose = int(input("health or unhealth (0 or 1) : "))
    if(choose==1):
        target = "unhealth"
        filename=["unhealth1.bmp", "unhealth2.bmp", "unhealth3.bmp", "unhealth4.bmp"]
        length = [50, 51.9, 55.6, 58.8]
        flag = False
    elif(choose==0):
        target = "health"
        filename=["health1.bmp", "health2.bmp"]
        length = [50, 50]
        flag = False
    else:
        print("please input the correct input!!!\n")


index = 0
data = []

for i, file in enumerate(filename):
    for index_of_circle in range(30):
        try:
            rgb=cv2.imread(file)
            todraw=cv2.imread(file)
            gray=cv2.imread(file,0)
            onebit=cv2.inRange(gray,90,130)
            sobel=Sobelfilter(gray)

            centers=HighCircle(todraw,sobel,onebit,index_of_circle,[20 , 40])#,True)
            center=centers[index_of_circle]
            lines,centerI=take_line(gray,center)

            Pixellength = length[i]/len(gray[0])
            inR,outR,allR=Radiuscal(todraw,lines,centerI,Pixellength,False)
            print("\nin=",inR)
            print("out=",outR)
            print(allR)
            data.append(allR)
            index += 1
        except:
            pass

np.savez(target, r = np.array(data))
print(index)
f = np.load(target+".npz")
print(f.files)
print(f[f.files[0]])