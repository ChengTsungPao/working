import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

def find(onebit,original_center):
    new_center=[0,0]
    new_center[0]=original_center[0]
    new_center[1]=original_center[1]
    r_biggest=0
    i=0
    j=0
    r_calc=0
    
    while onebit[original_center[1]+i,original_center[0]+j]==0:
        i+=1
    r_calc+=i
    i=0
    while onebit[original_center[1]-i,original_center[0]+j]==0:
        i+=1
    r_calc+=i
    
    r_biggest=r_calc
    
    while r_calc>0:
        i=0
        r_calc=0
        j-=1
        
        while onebit[original_center[1]+i,original_center[0]+j]==0:
            i+=1
        r_calc+=i
        i=0
        while onebit[original_center[1]-i,original_center[0]+j]==0:
            i+=1
        r_calc+=i
        if r_calc>r_biggest:
            new_center[0]=original_center[0]+j
            r_biggest=r_calc
    
    
    r_calc=r_biggest
    j=0
    while r_calc>0:
        r_calc=0
        j+=1
        i=0
        while onebit[original_center[1]+i,original_center[0]+j]==0:
            i+=1
        r_calc+=i
        i=0
        while onebit[original_center[1]-i,original_center[0]+j]==0:
            i+=1
        r_calc+=i
        if r_calc>r_biggest:
            new_center[0]=original_center[0]+j
            r_biggest=r_calc
    
    #==========
    r_biggest=0
    i=0
    j=0
    r_calc=0
    
    while onebit[original_center[1]+j,original_center[0]+i]==0:
        i+=1
    r_calc+=i
    i=0
    while onebit[original_center[1]+j,original_center[0]-i]==0:
        i+=1
    r_calc+=i
    
    r_biggest=r_calc
    
    while r_calc>0:
        i=0
        r_calc=0
        j-=1
        while onebit[original_center[1]+j,original_center[0]+i]==0:
            i+=1
        r_calc+=i
        i=0
        while onebit[original_center[1]+j,original_center[0]-i]==0:
            i+=1
        r_calc+=i
        if r_calc>r_biggest:
            new_center[1]=original_center[1]+j
            r_biggest=r_calc
    
    j=0
    r_calc=r_biggest
    while r_calc>0:
        i=0
        r_calc=0
        j+=1
        while onebit[original_center[1]+j,original_center[0]+i]==0:
            i+=1
        r_calc+=i
        i=0
        while onebit[original_center[1]+j,original_center[0]-i]==0:
            i+=1
        r_calc+=i
        if r_calc>r_biggest:
            new_center[1]=original_center[1]+j
            r_biggest=r_calc
    
    #print("r_biggest",r_biggest)
    return new_center

def trace(line_data,center):
    
    xx=np.array([i/100000 for i in range(len(line_data))])
    
    # plt.plot(xx,line_data)
    # plt.scatter(xx[center],line_data[center])    
    
    def fun(x,a,b,c,d,e,f,g,h,i,j,k):
        
        return k*x**10+j*x**9+i*x**8+h*x**7+g*x**6+f*x**5+a*x**4+b*x**3+c*x**2+d*x**1+e
    
    base=1.5/65# 兩成半徑預估
    rate=0.2/65
    n=1
    aa=fit(fun,xx[center:center+int(len(line_data)*(base+rate*n))],np.array(line_data[center:center+int(len(line_data)*(base+rate*n))]))[0]#,p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
    
    while fun(xx[center+int(len(line_data)*(base+n*rate))-1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10])>fun(xx[center+int(len(line_data)*(base+n*rate)-2)],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10]):
        n+=1
        aa=fit(fun,xx[center:center+int(len(line_data)*(base+n*rate))],np.array(line_data[center:center+int(len(line_data)*(base+n*rate))]))[0]#,p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
        #plt.plot(xx[center:center+int(len(line_data)*(base+n*rate))],fun(xx[center:center+int(len(line_data)*(base+n*rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10]))
    
    r=center+int(len(line_data)*(base+n*rate))-1
    while fun(xx[r],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10])<fun(xx[r-1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10]):
        r-=1
    
    n=1
    aa=fit(fun,xx[center-int(len(line_data)*(base+n*rate)):center],np.array(line_data[center-int(len(line_data)*(base+n*rate)):center]))[0]#,p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
    
    while fun(xx[center-int(len(line_data)*(base+n*rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10])>fun(xx[center-int(len(line_data)*(base+n*rate))+1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10]):
        n+=1
        aa=fit(fun,xx[center-int(len(line_data)*(base+n*rate)):center],np.array(line_data[center-int(len(line_data)*(base+n*rate)):center]))[0]#,p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
        #plt.plot(xx[center-int(len(line_data)*(base+n*rate)):center],fun(xx[center-int(len(line_data)*(base+n*rate)):center],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10]))
        #plt.show()
        
    l=center-int(len(line_data)*(base+n*rate))
    while fun(xx[l],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10])<fun(xx[l+1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10]):
        l+=1
    #plt.scatter(xx,f,color='r')
    #plt.plot(xx[center:center+int(len(line_data)*(base+n*rate))],fun(xx[center:center+int(len(line_data)*(base+n*rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]))
    # plt.scatter(xx[l],line_data[l])
    # plt.scatter(xx[r],line_data[r])
    # plt.show()
    
    return l,center,r

def Circle(imag,edges,Rrange,visible=True):
    
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
        if(a==6):
            cv2.circle(img,(c[0],c[1]),2,(255,0,0),3) # draw the center of the circle
            new=find(g,c)
            print(new)
    
            cv2.circle(img,(new[0],new[1]),2,(0,255,0),3)
            
            break
        
        
        a+=1
        
    
    
    cv2.circle(g,(c[0],c[1]),2,(255),3)
    cv2.circle(g,(new[0],new[1]),2,(0,255,0),3)
    
    cv2.imshow('i',g)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    cv2.imshow('i',img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    l,c,r=trace(gray[new[1]],new[0])
    print(l,c,r)