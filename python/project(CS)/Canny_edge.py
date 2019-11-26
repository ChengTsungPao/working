import cv2
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import copy

def Cannyedge(path,filename,visible=True):
    lowThreshold = 0
    max_lowThreshold = 40
    ratio = 3
    kernel_size = 3
    img = cv2.imread(path+filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), cv2.BORDER_DEFAULT)
    edges = cv2.Canny(blur_gray, lowThreshold, max_lowThreshold)
    if(visible):
        plt.imshow(edges, cmap='Greys_r')
        plt.show()
    return edges

def HighCircle(edges,Rrange,visible=True):
    img = edges
    cimg = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    #img = cv2.medianBlur(edges,5)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    center = []
    for i in circles[0,:]:  
        center.append([i[0],i[1]])
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
    if(visible):
        cv2.imshow('detected circles',cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return center

def Radiusline(image,center,visible=True):    
    L = image.convert("L")
    data = copy.copy(np.array(L))
    bright = [[] for i in range(4)]
    row = center[1]
    col = center[0]
    x , y = 0 , 0
    if(row > col):
        center_height = data[row][col]
        while row-col+x < len(data) and x < len(data):
            bright[0].append(data[row-col+x][0+x])
            bright[1].append(data[2*row-(row-col+x)][0+x])
            bright[2].append(data[row][x])
            bright[3].append(data[x][col])
            data[row-col+x][0+x] = 0
            data[2*row-(row-col+x)][0+x] = 0
            data[row][x] = 0
            data[x][col] = 0
            x += 1
            if(data[row][col]==0): data[row][col] = center_height
        for i in range(x,len(data)):
            bright[3].append(data[i][col])
            data[i][col] = 0
    else:
        center_height = data[row][col]
        while col-row+y < len(data) and y < len(data):
            bright[0].append(data[0+y][col-row+y])
            bright[1].append(data[2*row-y][col-row+y])
            bright[2].append(data[row][y])
            bright[3].append(data[y][col])
            data[0+y][col-row+y] = 0
            data[2*row-y][col-row+y] = 0
            data[row][y] = 0
            data[y][col] = 0
            y += 1
            if(data[row][col]==0): data[row][col] = center_height
        for i in range(y,len(data)):
            bright[2].append(data[row][i])
            data[row][i] = 0
    if(visible):
        plt.imshow(data)
        plt.show()
    return data,bright

def IndexVal(arr,s):
    init = 5
    if(s=="min"):
        index = [len(arr)//3+init,len(arr)*2//3-init]
        val = np.min(arr[index[0]:index[1]])
    elif(s=="max-left"):
        index = [0+init,len(arr)//3-init]
        val = np.max(arr[index[0]:index[1]])
    elif(s=="max-right"):
        index = [len(arr)*2//3+init,len(arr)-init]
        val = np.max(arr[index[0]:index[1]])
    else:
        print("please input the correct mpde")
        return 0
    return np.where(arr[index[0]:index[1]]==val)[0][0]+index[0],val 

def Radiuscal(bright,length,visible):
    init = -5
    InRadius , OutRadius = 0 , 0
    in_Radius = [[] for i in range(4)]
    out_Radius = [[] for i in range(4)]
    for index in range(len(bright)):
        r = np.linspace(0,length,len(bright[index]))
        min_center = IndexVal(bright[index],"min")
        max_right = IndexVal(bright[index],"max-right")
        max_left = IndexVal(bright[index],"max-left")

        in_height = np.mean([min_center[1],min_center[1],max_right[1],max_left[1]])
        out_height = np.mean([bright[index][init],bright[index][init],max_right[1],max_left[1]])
        
        for i in range(len(bright[index])-1):
            if((bright[index][i]-in_height)*(bright[index][i+1]-in_height)<=0 and i>=max_left[0] and i<=max_right[0]):
                in_Radius[index].append(i)
            elif(i==min_center[0]):
                in_Radius[index].append(i)            
            if((bright[index][i]-out_height)*(bright[index][i+1]-out_height)<=0):
                out_Radius[index].append(i)
            elif(i==min_center[0]):
                out_Radius[index].append(i)
        
        #print(in_Radius[index])
        #print(out_Radius[index])
        
        ans = [in_Radius[index][in_Radius[index].index(min_center[0])-1],in_Radius[index][in_Radius[index].index(min_center[0])+1]]
        for i in range(len(out_Radius[index])):
            if(out_Radius[index][i]>ans[0]):
                ans.append(out_Radius[index][i-1])
                break
        for j in range(i,len(out_Radius[index])):
            if(out_Radius[index][j]>ans[1]):
                ans.append(out_Radius[index][j])
                break
        #print(ans)
        if(index==0 or index==1):
            c = (2)**0.5
        else:
            c = 1
        r = c*r
        
        h = length/len(r)
        InRadius , OutRadius = InRadius+c*(ans[3]-ans[2])*h/4 ,  OutRadius+c*(ans[1]-ans[0])*h/4   

        if(visible):
            print("\nMin pos and value:\n   ", end="")
            print(r[min_center[0]],min_center[1])
            print("Max-right pos and value:\n   ", end="")
            print(r[max_right[0]],max_right[1])
            print("Max-left pos and value:\n   ", end="")
            print(r[max_left[0]],max_left[1])
            plt.subplot(221+index)
            plt.scatter([r[init],r[min_center[0]],r[max_right[0]],r[max_left[0]]],[bright[index][init],min_center[1],max_right[1],max_left[1]],color = "r")
            plt.title("Calculate Bright")
            plt.xlabel("width (\u03BCm)")
            plt.ylabel("brightness")
            #plt.plot([r[0],r[-1]],[bright[index][init],bright[index][init]],color = "r")
            plt.plot([r[max_left[0]],r[max_right[0]]],[in_height,in_height],label = "in")
            plt.plot([r[0],r[-1]],[out_height,out_height],label = "out")
            plt.plot(r,bright[index])
            plt.legend()
    if(visible):
        plt.tight_layout() 
        plt.show()
    return InRadius , OutRadius

filename = "test2.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/"
image = Image.open(path+filename)

Rrange = [230 , 250]
visible = True
length = 10

edges = Cannyedge(path,filename,visible)
center = HighCircle(edges,Rrange,visible)
data , bright = Radiusline(image,center[0],visible)
InRadius , OutRadius = Radiuscal(bright,length,visible)
print("---------------------------------------")
print(" InRadius : "+str(InRadius))
print("OutRadius : "+str(OutRadius))

  

