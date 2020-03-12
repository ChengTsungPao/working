import cv2
import numpy as np
import matplotlib.pyplot as plt
from find import find, trace, take_line
from filters import Sobelfilter


dirac=[[1,0],[0,1],[1,1],[1,-1]]


def showCV(title,image):
    cv2.imshow(title,image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def get_rough_centers(image_Sobel,Rrange):
    circles = cv2.HoughCircles(image_Sobel,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    center = []    
    for i in circles[0,:]:  
        center.append([i[0],i[1]])

    return center

def HighCircle(todraw,sobel,onebit,index_of_circle,Rrange,visible=False):
    circles = cv2.HoughCircles(sobel,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    center = []    
    for i in circles[0,:]:  
        rad = (i[0],i[1]),i[2],(0,255,0),2
        center.append([i[0],i[1]])
        if(visible):
            if(len(center)-1==index_of_circle):
                cv2.circle(todraw,(i[0],i[1]),i[2],(0,0,255),2) # draw the outer circle
                cv2.circle(todraw,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
    
    if(visible):
        cv2.imshow('detected circles',todraw)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    for i in range(len(center)):
        if(i==index_of_circle):
            #print(center[i])
            center[i] = find(onebit,center[i])
            #print(center[i])
            cv2.circle(todraw,(center[i][0],center[i][1]),2,(0,255,0),3) # draw the center of the circle
            break
    
    if(visible):
        cv2.imshow('detected circles',todraw)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return center

def Radiuscal(todraw,bright,center,Pixellength,visible=False):
    all_Radius = []

    init = 0
    InRadius , OutRadius = 0 , 0
    in_Radius = [[] for i in range(4)]
    out_Radius = [[] for i in range(4)]
    for index in range(len(bright)):
        start_offset=-int(center[index])
        ending=len(bright[index])+start_offset
        cv2.line(todraw,(center[0]+start_offset*dirac[index][0],center[1]+start_offset*dirac[index][1]),(center[0]+ending*dirac[index][0],center[1]+ending*dirac[index][1]),(255,255,255),2)
        
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
                cv2.circle(todraw,(center[0]+(start_offset+i)*dirac[index][0],center[1]+(start_offset+i)*dirac[index][1]),2,(0,0,255),3)
            
            elif(i==min_center[0]):
                in_Radius[index].append(i)
                #cv2.circle(todraw,(center[0]+(start_offset+i)*dirac[index][0],center[1]+(start_offset+i)*dirac[index][1]),2,(0,0,255),3)
                                        
            if((bright[index][i]-out_height)*(bright[index][i+1]-out_height)<=0):
                out_Radius[index].append(i)
                
            elif(i==min_center[0]):
                out_Radius[index].append(i)
                #cv2.circle(todraw,(center[0]+(start_offset+i)*dirac[index][0],center[1]+(start_offset+i)*dirac[index][1]),2,(0,0,255),3)
        # print(in_Radius)
        # print(out_Radius)       
        ans = [in_Radius[index][in_Radius[index].index(min_center[0])-1],in_Radius[index][in_Radius[index].index(min_center[0])+1]]
        for i in range(len(out_Radius[index])):
            if(out_Radius[index][i]>=ans[0]):
                ans.append(out_Radius[index][i-1])
                cv2.circle(todraw,(center[0]+(start_offset+ans[len(ans)-1])*dirac[index][0],center[1]+(start_offset+ans[len(ans)-1])*dirac[index][1]),2,(0,0,255),3)
                break
        
        for j in range(i,len(out_Radius[index])):
            if(out_Radius[index][j]>ans[1]):
                ans.append(out_Radius[index][j])
                cv2.circle(todraw,(center[0]+(start_offset+ans[len(ans)-1])*dirac[index][0],center[1]+(start_offset+ans[len(ans)-1])*dirac[index][1]),2,(0,0,255),3)
                break
        #print(ans)
        if(index==2 or index==3):
            c = (2)**0.5
        else:
            c = 1
        r = c*r

        h = Pixellength
        #all_Radius.append(c*(ans[1]-ans[0])*h)
        all_Radius.append(c*(ans[3]-ans[2])*h)
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
        showCV('hey',todraw)
    return InRadius , OutRadius , all_Radius

def draw_line(todraw,center,centerI,ls,rs,lines):
    for i in range(4):
        start_offset=-int(centerI[i])
        ending=len(lines[i])+start_offset
        cv2.line(todraw,(center[0]+start_offset*dirac[i][0],center[1]+start_offset*dirac[i][1]),(center[0]+ending*dirac[i][0],center[1]+ending*dirac[i][1]),(255,255,255),5)
    

if __name__=="__main__":

    #index_of_circle=11
    index_of_circle=0

    #all kinds of images we need======================
    file="test11.bmp"
    file="test12.bmp"
    rgb=cv2.imread(file)
    todraw=cv2.imread(file)
    gray=cv2.imread(file,0)
    onebit=cv2.inRange(gray,90,130)
    sobel=Sobelfilter(gray)

    # showCV("gray",gray)
    # showCV("onebit",onebit)
    # showCV("sobel",sobel)

    #=========================================
    centers=HighCircle(todraw,sobel,onebit,index_of_circle,[20 , 40])#,True)

    center=centers[index_of_circle]

    lines,centerI=take_line(gray,center)
    '''
    p=3

    plt.plot(lines[p])
    plt.scatter(centerI[p],lines[p][centerI[p]],c='r')
    plt.show()

    l,c,r=trace(lines[p],centerI[p],True)
    print(l,c)


    rs=[]
    ls=[]
    ci=[]
    for i in range(4):
        l,c,r=trace(lines[i],centerI[i])
        rs.append(r)
        ls.append(l)

    draw_line(rgb,center,centerI,ls,rs,lines)
    showCV('o',rgb)
    '''
    #l,c,r=trace(colum[0],colum[1],True)
    Pixellength = 50/len(gray[0])

    inR,outR,allR=Radiuscal(todraw,lines,centerI,Pixellength,True)
    print("\nin=",inR)
    print("out=",outR)

    #切出來================================
    '''
    newcircle_graph=[]
    lent=int(1*(rs[0]-ls[0]))
    #cv2.circle(rgb,(center[0],center[1]),lent,(255,0,255),2) # 圈出來
    showCV("hey",rgb)

    for j in range(2*lent):
        newcircle_graph.append([])
        for i in range(2*lent):
            newcircle_graph[j].append(rgb[center[1]-lent+j][center[0]-lent+i])
    newcircle_graph=np.array(newcircle_graph)


    gray=cv2.cvtColor(newcircle_graph,cv2.COLOR_BGR2GRAY)
    onebit=cv2.inRange(gray,90,110)
    sobel=Sobelfilter(gray)
    #print(newcircle_graph)
    showCV('hey',newcircle_graph)
    centers=HighCircle(newcircle_graph,sobel,onebit,[30 , 40],True)
    center=centers[index_of_circle]
    lines,centerI=take_line(gray,center)
    inR,outR=Radiuscal(newcircle_graph,lines,centerI,Pixellength,True)
    '''
