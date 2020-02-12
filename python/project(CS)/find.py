import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

def find(oneBit,center):
    new=[0,0]
    new[0]=c[0]
    new[1]=c[1]
    R=0
    i=0
    j=0
    r=0
    
    while g[c[1]+i,c[0]+j]==0:
        i+=1
    r+=i
    i=0
    while g[c[1]-i,c[0]+j]==0:
        i+=1
    r+=i
    
    R=r
    
    while r>0:
        i=0
        r=0
        j-=1
        
        while g[c[1]+i,c[0]+j]==0:
            i+=1
        r+=i
        i=0
        while g[c[1]-i,c[0]+j]==0:
            i+=1
        r+=i
        if r>R:
            new[0]=c[0]+j
            R=r
    
    
    r=R
    j=0
    while r>0:
        r=0
        j+=1
        i=0
        while g[c[1]+i,c[0]+j]==0:
            i+=1
        r+=i
        i=0
        while g[c[1]-i,c[0]+j]==0:
            i+=1
        r+=i
        if r>R:
            new[0]=c[0]+j
            R=r
    
    #==========
    R=0
    i=0
    j=0
    r=0
    
    while g[c[1]+j,c[0]+i]==0:
        i+=1
    r+=i
    i=0
    while g[c[1]+j,c[0]-i]==0:
        i+=1
    r+=i
    
    R=r
    
    while r>0:
        i=0
        r=0
        j-=1
        while g[c[1]+j,c[0]+i]==0:
            i+=1
        r+=i
        i=0
        while g[c[1]+j,c[0]-i]==0:
            i+=1
        r+=i
        if r>R:
            new[1]=c[1]+j
            R=r
    
    j=0
    r=R
    while r>0:
        i=0
        r=0
        j+=1
        while g[c[1]+j,c[0]+i]==0:
            i+=1
        r+=i
        i=0
        while g[c[1]+j,c[0]-i]==0:
            i+=1
        r+=i
        if r>R:
            new[1]=c[1]+j
            R=r
    
    #print("R",R)
    return new

def trace(gray,cen):
    f=gray[cen[1]]
    
    xx=np.array([i/100000 for i in range(len(f))])
    new = cen
    plt.plot(xx,f)
    plt.scatter(xx[new[0]],f[new[0]])
        
    
    def fun(x,a,b,c,d,e,f,g,h,ii):
        
        return ii*x**8+h*x**7+g*x**6+f*x**5+a*x**4+b*x**3+c*x**2+d*x**1+e
    
    base=2/65# 兩成半徑預估
    rate=0.1/65
    n=1
    aa=fit(fun,xx[new[0]:new[0]+int(len(f)*n*(base+rate))],np.array(f[new[0]:new[0]+int(len(f)*n*(base+rate))]),p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
    
    while fun(xx[new[0]+int(len(f)*n*(base+rate))-1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])>fun(xx[new[0]+int(len(f)*n*(base+rate)-2)],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
        n+=1
        aa=fit(fun,xx[new[0]:new[0]+int(len(f)*n*(base+rate))],np.array(f[new[0]:new[0]+int(len(f)*n*(base+rate))]),p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
        #plt.plot(xx[new[0]:new[0]+int(len(f)*n*(base+rate))],fun(xx[new[0]:new[0]+int(len(f)*n*(base+rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]))
    
    r=new[0]+int(len(f)*n*(base+rate))-1
    while fun(xx[r],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])<fun(xx[r-1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
        r-=1
    
    n=1
    aa=fit(fun,xx[new[0]-int(len(f)*n*(base+rate)):new[0]],np.array(f[new[0]-int(len(f)*n*(base+rate)):new[0]]),p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
    
    while fun(xx[new[0]-int(len(f)*n*(base+rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])>fun(xx[new[0]-int(len(f)*n*(base+rate))+1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
        n+=1
        aa=fit(fun,xx[new[0]-int(len(f)*n*(base+rate)):new[0]],np.array(f[new[0]-int(len(f)*n*(base+rate)):new[0]]),p0=[0,0,0.01,0.1,0.1,0.01,0.1,0.1,0.1])[0]
        #plt.plot(xx[new[0]-int(len(f)*n*(base+rate)):new[0]],fun(xx[new[0]-int(len(f)*n*(base+rate)):new[0]],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]))
        #plt.show()
        
    l=new[0]-int(len(f)*n*(base+rate))
    while fun(xx[l],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8])<fun(xx[l+1],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]):
        l+=1
    #plt.scatter(xx,f,color='r')
    #plt.plot(xx[new[0]:new[0]+int(len(f)*n*(base+rate))],fun(xx[new[0]:new[0]+int(len(f)*n*(base+rate))],aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8]))
    plt.scatter(xx[l],f[l])
    plt.scatter(xx[r],f[r])
    plt.show()
    
    return l,cen[0],r

def Circle(imag,edges,Rrange,visible=True):
    
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,30,param1=10,param2=20,minRadius=Rrange[0],maxRadius=Rrange[1])
    circles = np.uint16(np.around(circles))
    centers = []
    for i in circles[0,:]:
        
        centers.append([i[0],i[1]])
        if(visible):
            cv2.circle(img,(i[0],i[1]),i[2],(0,0,255),2) # draw the outer circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
    if(visible):
        cv2.imshow('detected circles',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return centers

# img=cv2.imread('multiple.bmp')
# gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# edge=cv2.Canny(gray, 1, 1)#cv2.inRange(gray,90,110)#cv2.Canny(gray, 1, 1)

# cen=Circle(img,edge,[30,40])

# g=cv2.inRange(gray,90,110) #用這個參數
# a=0
# for c in cen:
#     new=find(g,c)

#     cv2.circle(img,(new[0],new[1]),2,(0,255,0),3)
#     if(a==2):
#         break;
#     a+=1

# '''
# cv2.circle(g,(c[0],c[1]),2,(255),3)
# cv2.circle(g,(new[0],new[1]),2,(0,255,0),3)
# cv2.imshow('i',g)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# '''
# l,c,r=trace(gray,new)

# cv2.imshow('i',img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
