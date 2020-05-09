from copy import copy
import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mult
import os
from time import time

from draw_and_show import showCV

dfir=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
Rrange=[10,40]

#===================
def Sobelfilter(gray):
    sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
    image_Sobel = np.uint8(np.absolute(sobely))
    x = cv2.convertScaleAbs(sobelx)   
    y = cv2.convertScaleAbs(sobely)
    image_Sobel = cv2.addWeighted(x,0.5,y,0.5,0)
    return image_Sobel
#======================
    
#======================
def Cannyedge(gray):
    lowThreshold = 10
    max_lowThreshold = 10#40
    edges = cv2.Canny(gray, lowThreshold, max_lowThreshold)
    return edges
#======================

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

def cell_cut(graph,cell,Range):
    dimension=np.shape(graph)
    m=dimension[0]
    n=dimension[1]
    mid_m=(Range[1][1]+Range[1][0])//2
    mid_n=(Range[0][1]+Range[0][0])//2
    print(mid_m)
    if len(dimension)==3:
        new_graph=np.zeros([m,n,3],np.uint8)
    else:
        new_graph=np.zeros([m,n],np.uint8)
    m//=2
    n//=2
    s=0
    for i in cell:
        s+=graph[i[1]][i[0]]
        new_graph[i[1]-mid_m+m][i[0]-mid_n+n]=graph[i[1]][i[0]]
    
    
    return new_graph,float(s)/len(cell)


#dealing graph
def clear_white_edge(graph,white):
    white_line_wide=0
    m=len(graph)
    n=len(graph[0])
    
    def judge(value,white):
        if type(white)==int:
            if value==white:
                return True
            else:
                return False
        else:
            tf=False
            for i in range(len(white)):
                if value[i]==white[i]:
                    return True
            return False
    
    for j in range(n):
        i=0
        while i <m:
            if not judge(graph[i][j],white):
                break
            i+=1
        if i<m:
            break
        white_line_wide+=1
    return np.array([[graph[i][j] for j in range(white_line_wide,n)] for i in range(m)],np.uint8)

def trace_base_board(base):
    onebit=base[0]
    gray=base[1]
    thresh=base[2]
    if len(base)==3:
        m=[0,len(onebit)-1]
        n=[0,len(onebit[0])-1]
    else:
        Range=base[3]
        m=Range[1]
        n=Range[0]
    
    #the input Range is a 2*2 list, example:[[x_start,x_end],[y_start,y_end]]
    #bfs trace base board=============================
    mark=np.zeros([len(onebit),len(onebit[0])],bool)
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

def seperate_continent(base):
    onebit=base[0]
    thresh=base[1]
    Range=base[2]
    #the input Range is a 2*2 list, example:[[x_start,x_end],[y_start,y_end]]
    #bfs trace base board=============================
    mark=np.zeros([len(onebit),len(onebit[0])],bool)
    
    m=Range[1]
    n=Range[0]
    mid_m=(m[1]-m[0])//2
    mid_n=(n[1]-n[0])//2
    continent=[]
    stack=[]
    
    b=m[0]
    while b<=m[1]:
        s=0
        a=n[0]
        while a<=n[1]:
            if not mark[b][a] and onebit[b][a]:
                sep=np.zeros([len(onebit),len(onebit[0])],np.uint8)
                cell=[]
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
                        cell.append([j,i])
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
                    continent.append([sep,thresh,[xRange,yRange],cell])
            a+=1
        b+=1
    
    
    return continent

#====================================
def bfsfilter(gray, check):
    dthresh=20
    thresh=20
    final_continents=[]
    final_gray=[]
    m=len(gray)
    n=len(gray[0])
    Range=[[0,n-1],[0,m-1]]
    onebit=np.array([[255 for j in range(n)] for i in range(m)],np.uint8)
    
    base=[onebit,gray,thresh]
    onebit=trace_base_board(base)
    
    base=[onebit,thresh,Range]
    continents=seperate_continent(base)
    continents_gray=[cut_graph(gray,continents[i][0]) for i in range(len(continents))]
    
    p=mult.Pool(6 * check + (check == False))
    
    while len(continents)>0:
        #print("O")
        bases=[]
        for i in range(len(continents)):
            base=[continents[i][0],continents_gray[i],continents[i][1]+dthresh,continents[i][2]]
            bases.append(base)
        
        save_gray=copy(continents_gray)
        continents_gray=[]
        new_onebits=p.map(trace_base_board,bases)
        
        bases=[]
        
        for i in range(len(new_onebits)):
            base=[new_onebits[i],continents[i][1]+dthresh,continents[i][2]]
            bases.append(base)
        
        new_continents=p.map(seperate_continent,bases)
        save_continents=copy(continents)
        continents=[]
        
        for i in range(len(new_continents)):
            if len(new_continents[i])>1:
                for j in range(len(new_continents[i])):
                    
                    continents.append(new_continents[i][j])
                    continents_gray.append(cut_graph(gray,new_continents[i][j][0]))
            else:
                Range=bases[i][2]
                if Range[0][0] and Range[1][0] and Range[0][1]!=n-1 and Range[1][1]!=m-1:
                    final_continents.append(save_continents[i])
                    final_gray.append(save_gray[i])

    p.close()
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
#================================================== 

if __name__=='__main__':
    path=''#r"C:\CodingWorkSpace\blood\newnew\tide\datas\erythrocyte"
    bmp=".bmp"
    file="unhealth10.bmp"
    #file=health+str(wi+1)+bmp
    print(os.path.join(path,file))
    rgb=clear_white_edge(cv2.imread(os.path.join(path,file)),(255,255,255))
    Ogray=clear_white_edge(cv2.imread(os.path.join(path,file),0),255)
    gray=copy(Ogray)
    #16.710177278518678
    t=time()
    onebit,continents,grays=BFSfilter(gray)    
    t=time()-t
    print(t)
    showCV(onebit)
    
