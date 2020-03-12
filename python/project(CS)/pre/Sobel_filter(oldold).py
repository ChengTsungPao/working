import cv2
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import copy
from find import find, trace
index_of_circle = 5
def Sobelfilter(image_imread,visible=True):
    
    laplacian = cv2.Laplacian(image_imread,cv2.CV_64F)
    sobelx = cv2.Sobel(image_imread,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(image_imread,cv2.CV_64F,0,1,ksize=3)
    edges = np.uint8(np.absolute(sobely))
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    edges = cv2.addWeighted(x,0.5,y,0.5,0)

    if(visible):
        cv2.imshow('detected circles',edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return edges

rad = 0
circles = 0
def HighCircle(image_imread,edges,Rrange,visible=True):
    global circles
    global rad
    data_of_graph = []
    cimg = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    #img = cv2.medianBlur(edges,5)   
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])
    #circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1000,param1=10,param2=1,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    center = []    
    for i in circles[0,:]:  
        rad = (i[0],i[1]),i[2],(0,255,0),2
        center.append([i[0],i[1]])
        if(len(center)-1==index_of_circle):
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
    print(center)

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

start = []
filename = "test12.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/health/"
def Radiusline(image_PIL,center,Pixellength,visible=True):    #需要改有問題
    global start
    L = image_PIL.convert("L")
    #L = cv2.imread(path+filename,0)
    data = copy.copy(np.array(L))
    bright = [[] for i in range(4)]
    row = center[1]
    col = center[0]
    x , y = 0 , 0
    print(row,col)
    center_of_index = np.zeros(4,int)
    if(row > col):
        center_height = data[row][col]    
        start = [[row-col+x,0+x],[2*row-(row-col+x),0+x],[row,x],[x,col]]
        while x < max(len(data),len(data[0])):
            try:
                bright[0].append(data[row-col+x][0+x])
                data[row-col+x][0+x] = 0
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(row==row-col+x and col==x):
                    center_of_index[0] = x
            except:
                pass
            try:
                bright[1].append(data[2*row-(row-col+x)][0+x])
                data[2*row-(row-col+x)][0+x] = 0
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(2*row-(row-col+x)==row and col==x):
                    center_of_index[1] = x
            except:
                pass
            try:
                bright[2].append(data[row][x])
                data[row][x] = 0
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(col==x):
                    center_of_index[2] = x
            except:
                pass
            try:
                bright[3].append(data[x][col])
                data[x][col] = 0
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(row==x):
                    center_of_index[3] = x
            except:
                pass            
            x += 1
            
        for i in range(x,len(data)):
            bright[3].append(data[i][col])
            data[i][col] = 0
    else:
        center_height = data[row][col]
        start = [[0+y,col-row+y],[2*row-y,col-row+y],[row,y],[y,col]]
        while y < max(len(data),len(data[0])):
            try:           
                bright[0].append(data[0+y][col-row+y])
                data[0+y][col-row+y] = 0
                print(0+y,col-row+y)
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(row==y and col==col-row+y):
                    center_of_index[0] = y
            except:
                pass
            try: 
                bright[1].append(data[2*row-y][col-row+y])
                data[2*row-y][col-row+y] = 0
                print(2*row-y,col-row+y)
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(row==2*row-y and col==col-row+y):
                    center_of_index[1] = y
            except:
                pass
            try: 
                bright[2].append(data[row][y])
                data[row][y] = 0
                print(row,y)
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(col==y):
                    center_of_index[2] = y
            except:
                pass
            try: 
                bright[3].append(data[y][col])
                data[y][col] = 0
                print(y,col)
                if(data[row][col]==0): 
                    data[row][col] = center_height
                if(row==y):
                    center_of_index[3] = y
            except:
                pass
            y += 1
            print("--------------------------")
        for i in range(y,len(data)):
            bright[2].append(data[row][i])
            data[row][i] = 0
    if(visible):
        plt.imshow(data)
        plt.show()
    return data,bright,center_of_index

def IndexVal(arr,s,Pixellength):   #需要改別偷懶
    para = 3
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
        print("please input the correct mode")
        return 0
    return np.where(arr[index[0]:index[1]]==val)[0][0]+index[0],val 

pos = []
def Radiuscal(bright,center,Pixellength,visible):
    init = 0
    InRadius , OutRadius = 0 , 0
    in_Radius = [[] for i in range(4)]
    out_Radius = [[] for i in range(4)]
    for index in range(len(bright)):
        r = np.linspace(0,Pixellength*len(bright[index]),len(bright[index]))
        # min_center = IndexVal(bright[index],"min",Pixellength)
        # max_right = IndexVal(bright[index],"max-right",Pixellength)
        # max_left = IndexVal(bright[index],"max-left",Pixellength)

        print(len(bright[index]))
        print(center,len(bright[index]))
        for index in range(len(bright)):    
            print(len(bright[index]))
                
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
        
        # print(in_Radius[index])
        # print(out_Radius[index])
        # print("---------------------")
        # print(in_Radius)
        # print(out_Radius)
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
        
        pos.append(ans)
        h = Pixellength
        InRadius , OutRadius = InRadius+c*(ans[3]-ans[2])*h/4 ,  OutRadius+c*(ans[1]-ans[0])*h/4 
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
            plt.plot([r[max_left[0]],r[max_right[0]]],[in_height,in_height],label = "in")
            plt.plot([r[0],r[-1]],[out_height,out_height],label = "out")
            plt.plot(r,bright[index])
            plt.legend()
    if(visible):
        plt.tight_layout() 
        plt.show()
    return InRadius , OutRadius

#filename = "Height 091205.bmp"
filename = "test12.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/health/"
image_PIL = Image.open(path+filename)
image_imread = cv2.imread(path+filename,0)


Rrange = [30 , 40]  
#Rrange = [80 , 100]
#Rrange = [230 , 250] #單顆健康
#Rrange = [100 , 150]
visible = True
Pixellength = 50/image_PIL.size[0]
print(image_PIL.size)


edges = Sobelfilter(image_imread,visible)
center = HighCircle(image_imread,edges,Rrange,visible)
data , bright , center_of_index = Radiusline(image_PIL,center[index_of_circle],Pixellength,visible)
InRadius , OutRadius = Radiuscal(bright,center_of_index,Pixellength,False)
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

#plt.imshow(data)
#plt.show()
#cv2.circle(data,rad[0],rad[1],rad[2],rad[3])
cv2.imshow('detected circles',data)
cv2.waitKey(0)
cv2.destroyAllWindows()



