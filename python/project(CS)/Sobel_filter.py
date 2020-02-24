import cv2
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import copy
from findold import find, trace, take_line
index_of_circle = 0
def Sobelfilter(image_imread,visible=True):
    
    laplacian = cv2.Laplacian(image_imread,cv2.CV_64F)
    sobelx = cv2.Sobel(image_imread,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(image_imread,cv2.CV_64F,0,1,ksize=3)
    image_Sobel = np.uint8(np.absolute(sobely))
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    image_Sobel = cv2.addWeighted(x,0.5,y,0.5,0)

    if(visible):
        cv2.imshow('detected circles',image_Sobel)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return image_Sobel

def HighCircle(image_imread,image_Sobel,Rrange,visible=True):
    cimg = cv2.cvtColor(image_Sobel,cv2.COLOR_GRAY2BGR)
    #img = cv2.medianBlur(edges,5)   
    circles = cv2.HoughCircles(image_Sobel,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])
    #circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1000,param1=10,param2=1,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    center = []    
    for i in circles[0,:]:  
        rad = (i[0],i[1]),i[2],(0,255,0),2
        center.append([i[0],i[1]])
        if(len(center)-1==index_of_circle):
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle

    if(visible):
        cv2.imshow('detected circles',cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    g=cv2.inRange(image_imread,90,110)
    for i in range(len(center)):
        if(i==index_of_circle):
            center[i] = find(g,center[i])
            break
    return center

def Radiusline(image_imread,image_imread_gray,center,visible=True):    #需要改有問題  
    data = copy.deepcopy(image_imread_gray)
    bright = [[] for i in range(4)]
    center_of_index = np.zeros(4,int)
    tmp = take_line(image_imread,image_imread_gray,center)
    for i in range(4):
        bright[i] = copy.copy(tmp[i][0])
        center_of_index[i] = tmp[i][1]
    if(visible):
        plt.imshow(data)
        plt.show()
    return data,bright,center_of_index

def Radiuscal(bright,center,Pixellength,visible):
    init = 0
    InRadius , OutRadius = 0 , 0
    in_Radius = [[] for i in range(4)]
    out_Radius = [[] for i in range(4)]
    for index in range(len(bright)):
        r = np.linspace(0,Pixellength*len(bright[index]),len(bright[index]))
                
        tmp = trace(bright[index],center[index])
        min_center = tmp[1],bright[index][tmp[1]]
        max_left = tmp[0],bright[index][tmp[0]]
        max_right = tmp[2],bright[index][tmp[2]]

        in_height = np.mean([min_center[1],min_center[1],max_right[1],max_left[1]])
        out_height = np.mean([init,init,max_right[1],max_left[1]])
        
        for i in range(len(bright[index])-1):
            if((bright[index][i]-in_height)*(bright[index][i+1]-in_height)<=0 and i>=max_left[0] and i<=max_right[0]):
                in_Radius[index].append(i)
            elif(i==min_center[0]):
                in_Radius[index].append(i)            
            if((bright[index][i]-out_height)*(bright[index][i+1]-out_height)<=0):
                out_Radius[index].append(i)
            elif(i==min_center[0]):
                out_Radius[index].append(i)
        
        ans = [in_Radius[index][in_Radius[index].index(min_center[0])-1],in_Radius[index][in_Radius[index].index(min_center[0])+1]]
        for i in range(len(out_Radius[index])):
            if(out_Radius[index][i]>=ans[0]):
                ans.append(out_Radius[index][i-1])
                break
        for j in range(i,len(out_Radius[index])):
            if(out_Radius[index][j]>ans[1]):
                ans.append(out_Radius[index][j])
                break
        #print(ans)
        if(index==2 or index==3):
            c = (2)**0.5
        else:
            c = 1
        r = c*r

        h = Pixellength
        InRadius , OutRadius = InRadius+c*(ans[1]-ans[0])*h/4 ,  OutRadius+c*(ans[3]-ans[2])*h/4 
        #if(c*(ans[3]-ans[2])*h>InRadius):
        #    InRadius = c*(ans[3]-ans[2])*h
        #if(c*(ans[1]-ans[0])*h>OutRadius):
        #    OutRadius = c*(ans[1]-ans[0])*h

        if(visible):
            print("\nMin pos and value:\n   ", end="")
            print(r[min_center[0]],min_center[1])
            print("Max-right pos and value:\n   ", end="")
            print(r[max_right[0]],max_right[1])
            print("Max-left pos and value:\n   ", end="")
            print(r[max_left[0]],max_left[1])
            plt.subplot(221+index)
            plt.scatter([init,r[min_center[0]],r[max_right[0]],r[max_left[0]]],[init,min_center[1],max_right[1],max_left[1]],color = "r")
            plt.title("Calculate Bright")
            plt.xlabel("width (\u03BCm)")
            plt.ylabel("brightness")
            #plt.plot([r[0],r[-1]],[init,init],color = "r")
            plt.plot([r[ans[0]],r[ans[1]]],[in_height,in_height],"-o",label = "in")
            plt.plot([r[ans[2]],r[ans[3]]],[out_height,out_height],"-o",label = "out")
            #print(len(r),len(bright[index]))
            plt.plot(r,bright[index])
            plt.legend()
    if(visible):
        plt.tight_layout() 
        plt.show()
    return InRadius , OutRadius


filename = "test11.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/unhealth/"
filename = "test12.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/health/"
image_PIL = Image.open(path+filename)
image_imread = cv2.imread(path+filename)
image_imread_gray = cv2.imread(path+filename,0)

Rrange = [30 , 40]  
#Rrange = [80 , 100]
#Rrange = [230 , 250] #單顆健康
#Rrange = [100 , 150]
visible = True
Pixellength = 50/image_PIL.size[0]
print(image_PIL.size)
print(Pixellength)

image_Sobel = Sobelfilter(image_imread_gray,visible)
center = HighCircle(image_imread_gray,image_Sobel,Rrange,visible)
data , bright , center_of_index = Radiusline(image_imread,image_imread_gray,center[index_of_circle],visible)
InRadius , OutRadius = Radiuscal(bright,center_of_index,Pixellength,visible)
print("---------------------------------------")
print(" InRadius : "+str(InRadius))
print("OutRadius : "+str(OutRadius))



