import cv2
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import copy

def Cannyedge(path,filename,visible=True):
    lowThreshold = 10
    max_lowThreshold = 10#40
    #ratio = 3
    #kernel_size = 3
    img = cv2.imread(path+filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), cv2.BORDER_DEFAULT)
    edges = cv2.Canny(gray, lowThreshold, max_lowThreshold)
    #edges = gray
    if(visible):
        cv2.imshow('detected circles',edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return edges

rad = 0
circles = 0
def HighCircle(edges,Rrange,visible=True):
    global circles
    global rad
    img = edges
    cimg = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    #img = cv2.medianBlur(edges,5)   
    #circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=15,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1000,param1=10,param2=1,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    center = []    
    for i in circles[0,:]:  
        rad = (i[0],i[1]),i[2],(0,255,0),2
        center.append([i[0],i[1]])
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
    if(visible):
        cv2.imshow('detected circles',cimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return center
start = []
def Radiusline(image,center,visible=True):    #需要改有問題
    global start,flag
    L = image.convert("L")
    data = copy.copy(np.array(L))
    bright = [[] for i in range(4)]
    row = center[1]
    col = center[0]
    x , y = 0 , 0
    if(row > col):
        center_height = data[row][col]        
        start = [[row-col+x,0+x],[2*row-(row-col+x),0+x],[row,x],[x,col]]
        while row-col+x < len(data) and x < len(data):
            try:
                bright[0].append(data[row-col+x][0+x])
                data[row-col+x][0+x] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            try:
                bright[1].append(data[2*row-(row-col+x)][0+x])
                data[2*row-(row-col+x)][0+x] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            try:
                bright[2].append(data[row][x])
                data[row][x] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            try:
                bright[3].append(data[x][col])
                data[x][col] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass            
            x += 1
            
        for i in range(x,len(data)):
            bright[3].append(data[i][col])
            data[i][col] = 0
    else:
        center_height = data[row][col]
        start = [[0+y,col-row+y],[2*row-y,col-row+y],[row,y],[y,col]]
        while col-row+y < len(data) and y < len(data):
            try:           
                bright[0].append(data[0+y][col-row+y])
                data[0+y][col-row+y] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            try: 
                bright[1].append(data[2*row-y][col-row+y])
                data[2*row-y][col-row+y] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            try: 
                bright[2].append(data[row][y])
                data[row][y] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            try: 
                bright[3].append(data[y][col])
                data[y][col] = 0
                if(data[row][col]==0): data[row][col] = center_height
            except:
                pass
            y += 1
            
        for i in range(y,len(data)):
            bright[2].append(data[row][i])
            data[row][i] = 0
    if(visible):
        plt.imshow(data)
        plt.show()
    return data,bright

def IndexVal(arr,s,Pixellength):   #需要改別偷懶
    para = 4
    if(s=="min"):
        index = [len(arr)//3,len(arr)*2//3]
        val = np.min(arr[index[0]:index[1]])
    elif(s=="max-left"):
        index = [len(arr)//3,len(arr)*2//3]
        val = np.min(arr[index[0]:index[1]])
        tmp = np.where(arr[index[0]:index[1]]==val)[0][0]+index[0]

        index = [tmp-int(para/Pixellength),tmp]
        val = np.max(arr[index[0]:index[1]])
    elif(s=="max-right"):
        index = [len(arr)//3,len(arr)*2//3]
        val = np.min(arr[index[0]:index[1]])
        tmp = np.where(arr[index[0]:index[1]]==val)[0][0]+index[0]

        index = [tmp,tmp+int(para/Pixellength)]
        val = np.max(arr[index[0]:index[1]])
    else:
        print("please input the correct mpde")
        return 0
    return np.where(arr[index[0]:index[1]]==val)[0][0]+index[0],val 
pos = []
which_index = []
max = 0
def Radiuscal(bright,Pixellength,visible):
    global which_index,max
    init = 0
    InRadius , OutRadius = 0 , 0
    in_Radius = [[] for i in range(4)]
    out_Radius = [[] for i in range(4)]
    for index in range(len(bright)):
        r = np.linspace(0,Pixellength*len(bright[index]),len(bright[index]))
        min_center = IndexVal(bright[index],"min",Pixellength)
        max_right = IndexVal(bright[index],"max-right",Pixellength)
        max_left = IndexVal(bright[index],"max-left",Pixellength)

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
        
        # print(in_Radius[index])
        # print(out_Radius[index])
        
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
        # print(abs(ans[1]-min_center[0])*c,abs(ans[0]-min_center[0])*c)
        # if(abs(ans[1]-min_center[0])*c>max or abs(ans[0]-min_center[0])*c>max):
        #     if(abs(ans[1]-min_center[0])*c < abs(ans[0]-min_center[0])*c):
        #         which_index = [index,0]
        #         max = abs(ans[0]-min_center[0])*c
        #     else:
        #         which_index = [index,1]
        #         max = abs(ans[1]-min_center[0])*c

        print(abs(ans[3]-min_center[0])*c,abs(ans[2]-min_center[0])*c)
        if(abs(ans[3]-min_center[0])*c>max or abs(ans[2]-min_center[0])*c>max):
            if(abs(ans[3]-min_center[0])*c < abs(ans[2]-min_center[0])*c):
                which_index = [index,0]
                max = abs(ans[2]-min_center[0])*c
            else:
                which_index = [index,1]
                max = abs(ans[3]-min_center[0])*c


        pos.append(ans)
        h = Pixellength
        InRadius , OutRadius = InRadius+c*(ans[3]-ans[2])*h/4 ,  OutRadius+c*(ans[1]-ans[0])*h/4 
        #if(c*(ans[3]-ans[2])*h>InRadius):
        #    which_ = c*(ans[3]-ans[2])*h
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
            plt.plot([r[max_left[0]],r[max_right[0]]],[in_height,in_height],label = "in")
            plt.plot([r[0],r[-1]],[out_height,out_height],label = "out")
            plt.plot(r,bright[index])
            plt.legend()
    if(visible):
        plt.tight_layout() 
        plt.show()
    return InRadius , OutRadius

def adjust(image,Pixellength,center,which_index):
    k = 5
    if(which_index[0]==0 and which_index[1]==0):
        #++
        center[0][0] -= k
        center[0][1] -= k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==0 and which_index[1]==1):
        #後
        center[0][0] += k
        center[0][1] += k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==1 and which_index[1]==0):
        #-+
        center[0][0] += k
        center[0][1] -= k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==1 and which_index[1]==1):
        center[0][0] -= k
        center[0][1] += k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==2 and which_index[1]==0):
        #0+
        center[0][1] -= k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==3 and which_index[1]==1):
        center[0][1] += k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==3 and which_index[1]==0):
        #+0
        center[0][0] -= k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    elif(which_index[0]==3 and which_index[1]==1):
        center[0][0] += k
        data , bright = Radiusline(image,center[0],visible)
        InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
        print(" InRadius : "+str(InRadius))
        print("OutRadius : "+str(OutRadius))
    return center


#filename = "Height 091205.bmp"
filename = "test2.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/health/pre/"
image = Image.open(path+filename)

#Rrange = [40 , 50]
#Rrange = [80 , 100]
Rrange = [230 , 250]
#Rrange = [100 , 150]
visible = True
Pixellength = 10/image.size[0]
print(Pixellength)
print(image.size)
edges = Cannyedge(path,filename,visible)
center = HighCircle(edges,Rrange,visible)
data , bright = Radiusline(image,center[0],visible)
InRadius , OutRadius = Radiuscal(bright,Pixellength,visible)
print("---------------------------------------")
print(" InRadius : "+str(InRadius))
print("OutRadius : "+str(OutRadius))

def dot(x,y,k):
    data[x][y] = 0
    if k>=5: return
    dot(x+1,y,k+1)
    dot(x,y+1,k+1)
    dot(x,y-1,k+1)
    dot(x-1,y,k+1)
    dot(x+1,y+1,k+1)
    dot(x-1,y-1,k+1)
    dot(x-1,y+1,k+1)
    dot(x+1,y-1,k+1)

for i in range(4):
    dot(start[0][0]+pos[0][i],start[0][1]+pos[0][i],0)
for i in range(4):
    dot(start[1][0]-pos[1][i],start[1][1]+pos[1][i],0)
for i in range(4):
    dot(start[2][0],start[2][1]+pos[2][i],0)
for i in range(4):
    dot(start[3][0]+pos[3][i],start[3][1],0)
dot(center[0][0],center[0][1],0)

#plt.imshow(data)
#plt.show()
a = copy.copy(data)
plt.imshow(a)
plt.show()
cv2.circle(a,rad[0],rad[1],rad[2],rad[3])
cv2.imshow('detected circles',a)
cv2.waitKey(0)
cv2.destroyAllWindows()

# print(which_index)
# for i in range(100):
#     def dot(x,y,k):
#         data[x][y] = 0
#         if k>=5: return
#         dot(x+1,y,k+1)
#         dot(x,y+1,k+1)
#         dot(x,y-1,k+1)
#         dot(x-1,y,k+1)
#         dot(x+1,y+1,k+1)
#         dot(x-1,y-1,k+1)
#         dot(x-1,y+1,k+1)
#         dot(x+1,y-1,k+1)

#     for i in range(4):
#         dot(start[0][0]+pos[0][i],start[0][1]+pos[0][i],0)
#     for i in range(4):
#         dot(start[1][0]-pos[1][i],start[1][1]+pos[1][i],0)
#     for i in range(4):
#         dot(start[2][0],start[2][1]+pos[2][i],0)
#     for i in range(4):
#         dot(start[3][0]+pos[3][i],start[3][1],0)
#     dot(center[0][0],center[0][1],0)

#     #plt.imshow(data)
#     #plt.show()
#     a = copy.copy(data)
#     plt.imshow(a)
#     plt.show()
#     cv2.circle(a,rad[0],rad[1],rad[2],rad[3])
#     cv2.imshow('detected circles',a)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     center = adjust(image,Pixellength,center,which_index)
