import cv2
import numpy as np
from copy import copy
import matplotlib.pyplot as plt


def Sobelfilter(gray):
    sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
    image_Sobel = np.uint8(np.absolute(sobely))
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    image_Sobel = cv2.addWeighted(x,0.5,y,0.5,0)
    return image_Sobel

def Cannyedge(gray):
    lowThreshold = 10
    max_lowThreshold = 10#40
    edges = cv2.Canny(gray, lowThreshold, max_lowThreshold)
    return edges

def bfsfilter(gray, Rrange):

    dfir=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
    thresh=20
    dthresh=20

    def reset_graph(boolean_graph,Range):
        m=Range[1]
        n=Range[0]
        for i in range(m[0],m[1]+1):
            for j in range(n[0],n[1]+1):
                mark[i][j]=False

    def cut_graph(graph,onebit):
        dimension=np.shape(graph)
        if len(dimension)==3:
            zero=(0,0,0)
        else:
            zero=0
        m=dimension[0]
        n=dimension[1]
        new_graph=[]
        
        for i in range(m):
            new_graph.append([])
            for j in range(n):
                if onebit[i][j]:
                    new_graph[i].append(graph[i][j])
                else:
                    new_graph[i].append(zero)
        
        return np.array(new_graph,np.uint8)

    def trace_base_board(onebit,gray,thresh,Range=False):
        #the input Range is a 2*2 list, example:[[x_start,x_end],[y_start,y_end]]
        #bfs trace base board=============================
        mark=np.zeros([len(onebit),len(onebit[0])],bool)
        if not Range:
            m=[0,len(onebit)-1]
            n=[0,len(onebit[0])-1]
        else:
            m=Range[1]
            n=Range[0]
        new_onebit=copy(onebit)
        mu=[[0,1],[1,0],[0,-1],[-1,0]]
        start=[[n[0],m[0]] for i in range(2)]+[[n[1],m[1]] for i in range(2)]
        ml=m[1]-m[0]+1
        nl=n[1]-n[0]+1
        ll=[ml,nl]*2
        
        stack=[]
        
        for p in range(4):
            a=start[p][0]-mu[p][0]
            b=start[p][1]-mu[p][1]
            for h in range(ll[p]):
                
                a+=mu[p][0]
                b+=mu[p][1]
                if mark[b][a]:
                    continue
                
                elif gray[b][a]<thresh:
                    mark[b][a]=True
                    stack.append([a,b])
                    while len(stack)>0:
                        val=stack.pop(0)
                        i=val[1]
                        j=val[0]
            
                        if gray[i][j]<thresh:
                            new_onebit[i][j]=0
                            for k in range(4):
                                ii=i+dfir[k][1]
                                jj=j+dfir[k][0]
                                if ii<m[1]+1 and jj<n[1]+1 and ii>m[0]-1 and jj>n[0]-1:
                                    if mark[ii][jj]==False:
                                        mark[ii][jj]=True
                                        stack.append([jj,ii])
        
        return new_onebit

    def seperate_continent(onebit,Range,thresh):
        #the input Range is a 2*2 list, example:[[x_start,x_end],[y_start,y_end]]
        #bfs trace base board=============================
        mark=np.zeros([len(onebit),len(onebit[0])],bool)
        
        m=Range[1]
        n=Range[0]
        
        continent=[]
        stack=[]
        
        b=m[0]
        while b<=m[1]:
            a=n[0]
            while a<=n[1]:
                if not mark[b][a] and onebit[b][a]:
                    sep=np.zeros([len(onebit),len(onebit[0])],np.uint8)
                    xRange=[n[1],n[0]]
                    yRange=[m[1],m[0]]
                    mark[b][a]=True
                    stack.append([a,b])
                    while len(stack)>0:
                        val=stack.pop(0)
                        i=val[1]
                        j=val[0]
            
                        if onebit[i][j]:
                            sep[i][j]=255
                            if j<xRange[0]:
                                xRange[0]=j
                            elif j>xRange[1]:
                                xRange[1]=j
                            
                            if i<yRange[0]:
                                yRange[0]=i
                            elif i>yRange[1]:
                                yRange[1]=i
                            
                            for k in range(4):
                                ii=i+dfir[k][1]
                                jj=j+dfir[k][0]
                                if ii<m[1]+1 and jj<n[1]+1 and ii>m[0]-1 and jj>n[0]-1:
                                    if mark[ii][jj]==False:
                                        mark[ii][jj]=True
                                        stack.append([jj,ii])
                    if yRange[1]-yRange[0]>2*Rrange[0] and xRange[1]-xRange[0]>2*Rrange[0]:
                        continent.append([sep,[xRange,yRange],thresh])
                a+=1
            b+=1       
        
        return continent

    final_continents=[]
    final_gray=[]
    m=len(gray)
    n=len(gray[0])
    Range=[[0,n-1],[0,m-1]]
    
    onebit=np.array([[255 for j in range(n)] for i in range(m)],np.uint8)
    onebit=trace_base_board(onebit,gray,thresh)
    continents=seperate_continent(onebit,Range,thresh)
    continents_gray=[cut_graph(gray,continents[i][0]) for i in range(len(continents))]
    
    while len(continents)>0:
        old_continent=continents.pop(-1)
        old_gray=continents_gray.pop(-1)
        new_thresh=old_continent[2]+dthresh
        Range=old_continent[1]
        new_onebit=trace_base_board(old_continent[0],old_gray,new_thresh,Range)
        new_continents=seperate_continent(new_onebit,Range,new_thresh)
        if len(new_continents)>1:
            while len(new_continents)>0:
                new_continent=new_continents.pop(0)
                continents.append(new_continent)
                continents_gray.append(cut_graph(old_gray,new_continent[0]))
        else:
            if Range[0][0] and Range[1][0] and Range[0][1]!=n-1 and Range[1][1]!=m-1:
                        final_continents.append(old_continent)
                        final_gray.append(old_gray)
    
    final_onebit=np.array([[0 for j in range(n)] for i in range(m)],np.uint8)
    for i in final_continents:
        s=0
        count=0
        for j in range(len(i[0])):
            for k in range(len(i[0][0])):
                if i[0][j][k]:
                    s+=gray[j][k]
                    count+=1
                    final_onebit[j][k]=255
                
        i.append(s/count)
    return final_onebit,final_continents,final_gray