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


#show
def showCV(title,image):
    cv2.imshow(title,image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def draw_circles(todraw,all_x_y_r,color,need_center=True,draw_in_copy=False):
    if draw_in_copy:    to_draw=copy(todraw)
    else:   to_draw=todraw
    for i in all_x_y_r:
        #cv2.circle(to_draw,(i[0],i[1]),i[2],color,2) # draw the outer circle
        if need_center:
            cv2.circle(to_draw,(i[0],i[1]),2,color,3) # draw the center of the circle
    return to_draw


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




def reset_graph(boolean_graph,Range):
    m=Range[1]
    n=Range[0]
    for i in range(m[0],m[1]+1):
        for j in range(n[0],n[1]+1):
            mark[i][j]=False


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
                
                '''sep=np.zeros([len(onebit),len(onebit[0])],np.uint8)
                for ind in cell:
                    sep[cell[1]-mid_m][cell[0]-mid_m]=255
                '''
                if yRange[1]-yRange[0]>2*Rrange[0] and xRange[1]-xRange[0]>2*Rrange[0]:
                    continent.append([sep,[xRange,yRange],thresh,cell])
            a+=1
        b+=1
    
    
    return continent

def continent_filter(gray,thresh):
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
                #grayy,new_continent[0]=cell_cut_move(old_gray,new_continent[0],new_continent[3],new_continent[1])
                continents.append(new_continent)
                #continents_gray.append(grayy)
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
#-#-#-#-#-#-#-#-#main------------------------------------------

#all kinds of images we need======================
#base_graph,
health="health"
unhealth="unhealth"
for wi in range(0,1):
    path=''#r"C:\CodingWorkSpace\blood\newnew\tide\datas\erythrocyte"
    bmp=".bmp"
    file="bad1.bmp"
    #file=health+str(wi+1)+bmp
    print(os.path.join(path,file))
    rgb=clear_white_edge(cv2.imread(os.path.join(path,file)),(255,255,255))
    Ogray=clear_white_edge(cv2.imread(os.path.join(path,file),0),255)
    gray=copy(Ogray)
    #length, hight about values===================================
    m=len(gray)
    n=len(gray[0])
    real_length=80
    o_length=50
    Pixellength = real_length/n
    Rrange=[10,40]
    
    Range=[[0,n-1],[0,m-1]]
    
    #operating_graph
    todraw=copy(rgb)
    t=time()
    onebit,continents,grays=continent_filter(gray,thresh)
    t=time()-t
    print(t)
    
    