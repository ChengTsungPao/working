import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit


#use to correct the center of the RBC
def find(onebit,original_center):
    
    #declare new center=================
    new_center=[]
    for i in range(2):
        new_center.append(original_center[i])
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
    
    # def fun(x,a,b,c,d,e,f,g,h,i):
        
    #     return i*x**8+h*x**7+g*x**6+f*x**5+a*x**4+b*x**3+c*x**2+d*x**1+e

    def fun(x,c,d,e):
        
        return c*x**2+d*x**1+e
    
    #32 c r 差
    
    base=20
    d=1
    
    #fitting right hand========================================
    end=center+base+d+1
    aa=fit(fun,xx[center:end],np.array(line_data[center:end]))[0]

    while fun(xx[end-1],aa[0],aa[1],aa[2])>fun(xx[end-2],aa[0],aa[1],aa[2]):
    #while fun(xx[end-1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])>fun(xx[end-2],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
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

    while fun(xx[start],aa[0],aa[1],aa[2])>fun(xx[start+1],aa[0],aa[1],aa[2]):
    #while fun(xx[start],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])>fun(xx[start+1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
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


if __name__=="__main__":
    img=cv2.imread('test12.bmp')
    gray=cv2.imread('test12.bmp',0)
    #gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=gray
    #edge=cv2.Canny(gray, 1, 1)#cv2.inRange(gray,90,110)#cv2.Canny(gray, 1, 1)
    
    laplacian = cv2.Laplacian(img,cv2.CV_64F)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
    edges = np.uint8(np.absolute(sobely))
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    edge = cv2.addWeighted(x,0.5,y,0.5,0)
    
    img=cv2.imread("test12.bmp")
    cen=Circle(img,edge,[30,40])
    g=cv2.inRange(gray,90,110)
    a=0
    for c in cen:
        if(a==0):
            cv2.circle(img,(c[0],c[1]),2,(255,0,0),3) # draw the center of the circle
            new=find(g,c)
    
            cv2.circle(img,(new[0],new[1]),2,(0,255,0),3)
            
            break
        
        
        a+=1
        
    
    
    cv2.circle(g,(c[0],c[1]),2,(255),3)
    cv2.circle(g,(new[0],new[1]),2,(0,255,0),3)
    '''
    cv2.imshow('i',g)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('i',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

