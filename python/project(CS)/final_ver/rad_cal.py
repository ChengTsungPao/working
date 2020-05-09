import cv2
import numpy as np
import matplotlib.pyplot as plt
from copy import copy
from find import find, trace, take_line

import pickle
import os
from time import time

#diraction step
dfir=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
thresh=20
dthresh=20
dirac=[[1,0],[0,1],[1,1],[1,-1]]

smallist_area=10



#use to correct the center of the RBC
def find(onebit,original_center,bw='b'):
    new_center=[]
    for i in range(2):
        new_center.append(original_center[i])
    
    if bw=='b':
        #declare new center=================
        #===================================
        dire=[1,-1]
        
        #correct horizontal position
        r_biggest=0
        r_temp=0
        i=0 #perpendicular index
        j=0 #horizonrtal index
        
        for k in range(2):
            while onebit[original_center[1]+i*dire[k],original_center[0]]==0:
                i+=1
            r_temp+=i
            i=0
    
        r_biggest=r_temp
        
        for w in range(2):
            while r_temp>0:
                r_temp=0
                j+=dire[w]
                
                for k in range(2):
                    while onebit[original_center[1]+i*dire[k],original_center[0]+j]==0:
                        i+=1
                    r_temp+=i
                    i=0
                
                if r_temp>r_biggest:
                    new_center[0]=original_center[0]+j
                    r_biggest=r_temp
            
            r_temp=r_biggest
        
        #correct perpendicular position
        r_biggest=0
        r_temp=0
        i=0 #horizonrtal index
        j=0 #perpendicular index
        
        #correct horizontal position
        for k in range(2):
            while onebit[original_center[1],original_center[0]+i*dire[k]]==0:
                i+=1
            r_temp+=i
            i=0
    
        r_biggest=r_temp
        
        for w in range(2):
            while r_temp>0:
                r_temp=0
                j+=dire[w]
                
                for k in range(2):
                    while onebit[original_center[1]+j,original_center[0]+i*dire[k]]==0:
                        i+=1
                    r_temp+=i
                    i=0
                
                if r_temp>r_biggest:
                    new_center[1]=original_center[1]+j
                    r_biggest=r_temp
            
            r_temp=r_biggest
        
    else:
        dire=[1,-1]
        
        #correct horizontal position
        r_biggest=0
        r_temp=0
        i=0 #perpendicular index
        j=0 #horizonrtal index
        
        for k in range(2):
            while onebit[original_center[1]+i*dire[k],original_center[0]]==255:
                i+=1
            r_temp+=i
            i=0
    
        r_biggest=r_temp
        
        for w in range(2):
            while r_temp>0:
                r_temp=0
                j+=dire[w]
                
                for k in range(2):
                    while onebit[original_center[1]+i*dire[k],original_center[0]+j]==255:
                        i+=1
                    r_temp+=i
                    i=0
                
                if r_temp>r_biggest:
                    new_center[0]=original_center[0]+j
                    r_biggest=r_temp
            
            r_temp=r_biggest
        
        #correct perpendicular position
        r_biggest=0
        r_temp=0
        i=0 #horizonrtal index
        j=0 #perpendicular index
        
        #correct horizontal position
        for k in range(2):
            while onebit[original_center[1],original_center[0]+i*dire[k]]==255:
                i+=1
            r_temp+=i
            i=0
    
        r_biggest=r_temp
        
        for w in range(2):
            while r_temp>0:
                r_temp=0
                j+=dire[w]
                
                for k in range(2):
                    while onebit[original_center[1]+j,original_center[0]+i*dire[k]]==255:
                        i+=1
                    r_temp+=i
                    i=0
                
                if r_temp>r_biggest:
                    new_center[1]=original_center[1]+j
                    r_biggest=r_temp
            
            r_temp=r_biggest
            
            
    return new_center

def take_line(gray,center):
    ly=len(gray) #length of colum
    lx=len(gray[0]) #length of row
    
    line=[]
    centers=[int(center[0]),int(center[1])]
    
    #row line====================================
    row=[]
    for i in range(lx):
        row.append(int(gray[center[1]][i]))
    
    #colum line====================================
    colum=[]
    for i in range(ly):
        colum.append(int(gray[i][center[0]]))
       
    #slash line of positive slope====================================
    slope_p=[]
    temp_center=[]
    if center[0]<center[1]:
        c=center[0]
    else:
        c=center[1]
    
    centers.append(c)
    for i in range(2):
        temp_center.append(center[i]-c)

    while temp_center[0]<lx-1 and temp_center[1]<ly-1:
        slope_p.append(gray[temp_center[1]][temp_center[0]])
        for i in range(2):
            temp_center[i]+=1
    
    #slash line of negative slope====================================
    slope_n=[]
        
    for i in range(2):
        temp_center[i]=center[i]
    
    count=0
    while temp_center[0]>0 and temp_center[1]<ly-1:
        temp_center[0]-=1
        temp_center[1]+=1
        count+=1
    centers.append(count)
    
    while temp_center[0]<lx-1 and temp_center[1]>0:
        slope_n.append(gray[temp_center[1]][temp_center[0]])
        
        temp_center[0]+=1
        temp_center[1]-=1
    
    line.append(row)  
    line.append(colum)
    line.append(slope_p)  
    line.append(slope_n)
    
    return line,centers

def trace(line_data,center,check=False):
    
    xx=np.array([i/100000 for i in range(len(line_data))])        
    
    def fun(x,a,b,c,d,e,f,g,h,i):
        
        return i*x**8+h*x**7+g*x**6+f*x**5+a*x**4+b*x**3+c*x**2+d*x**1+e
    
    #32 c r 差
    
    base=20
    d=1
    
    #fitting right hand========================================
    end=center+base+d+1
    aa=fit(fun,xx[center:end],np.array(line_data[center:end]))[0]
    
    while fun(xx[end-1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])>fun(xx[end-2],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
        end+=d
        aa=fit(fun,xx[center:end],np.array(line_data[center:end]))[0]
        #plt.plot(xx[center:center+int(len(line_data)*(base+n*rate))],fun(xx[center:center+int(len(line_data)*(base+n*rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]))
    
    r=end-1
    tem=r
    big=line_data[r]
    for i in range(center,r):
        if line_data[i]>big:
            big=line_data[i]
            tem=i
    
    r=tem
    #fitting left hand===========================================
    start=center-(base+d)
    aa=fit(fun,xx[start:center+1],np.array(line_data[start:center+1]))[0]
    
    while fun(xx[start],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])>fun(xx[start+1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
        start-=d
        aa=fit(fun,xx[start:center+1],np.array(line_data[start:center+1]))[0]
        #plt.plot(xx[center-int(len(line_data)*(base+n*rate)):center],fun(xx[center-int(len(line_data)*(base+n*rate)):center],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]))
        #plt.show()
        
    l=start
    tem=l
    big=line_data[l]
    
    for i in range(l+1,center+1):
        if line_data[i]>big:
            big=line_data[i]
            tem=i
    l=tem
    
    if check:
        plt.plot(xx,line_data)
        plt.scatter(xx[center],line_data[center])
        plt.scatter(xx[l],line_data[l])
        plt.scatter(xx[r],line_data[r])
        plt.show()
    
    return l,center,r

def Circle(imag,edges,Rrange,visible=False):
    
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    centers = []
    for i in circles[0,:]:
        
        centers.append([i[0],i[1]])
        if(visible):
            cv2.circle(imag,(i[0],i[1]),i[2],(0,0,255),2) # draw the outer circle
            cv2.circle(imag,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
    if(visible):
        cv2.imshow('detected circles',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return centers


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
        # all_Radius.append((ans[1]-ans[0])/(ans[3]-ans[2]))

        # all_Radius.append(c*(ans[1]-ans[0])*h)
        # all_Radius.append(c*(ans[3]-ans[2])*h)

        
        

        all_Radius.append(c*abs(ans[0]-min_center[0])*h)
        all_Radius.append(c*abs(max_right[0]-min_center[0])*h)
        all_Radius.append(c*abs(ans[1]-min_center[0])*h)
        all_Radius.append(c*abs(ans[2]-min_center[0])*h)
        all_Radius.append(c*abs(max_left[0]-min_center[0])*h)
        all_Radius.append(c*abs(ans[3]-min_center[0])*h)


        # all_Radius.append(abs(bright[index][ans[0]]-min_center[1]))
        # all_Radius.append(abs(max_right[1]-min_center[1]))
        # all_Radius.append(abs(bright[index][ans[1]]-min_center[1]))
        # all_Radius.append(abs(bright[index][ans[2]]-min_center[1]))
        # all_Radius.append(abs(max_left[1]-min_center[1]))
        # all_Radius.append(abs(bright[index][ans[3]]-min_center[1]))


        # all_Radius.append(min_center[1])
        # all_Radius.append(max_right[1])        
        # all_Radius.append(max_left[1])

        InRadius , OutRadius = InRadius+c*(ans[1]-ans[0])*h/4 ,  OutRadius+c*(ans[3]-ans[2])*h/4 

        #all_Radius = [InRadius , OutRadius]



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
        plt.clf()
        showCV('hey',todraw)
    return InRadius , OutRadius , all_Radius
