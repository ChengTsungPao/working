import cv2
import numpy as np
import matplotlib.pyplot as plt
from copy import copy
from find import find, trace, take_line

#show
def showCV(title,image):
    cv2.imshow(title,image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def draw_circles(todraw,all_x_y_r,color,draw_in_copy=False):
    if draw_in_copy:    to_draw=copy(todraw)
    else:   to_draw=todraw
    for i in all_x_y_r:
        cv2.circle(to_draw,(i[0],i[1]),i[2],color,2) # draw the outer circle
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


#diraction step
dfir=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
dthresh=5
smallist_area=10

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
    #new_gray=copy(gray)   #leave?
    mu=[[1,0],[0,1],[-1,0],[0,-1]]
    start=[[m[0],n[0]],[m[0],n[0]],[m[1],n[1]],[m[1],n[1]]]
    ml=m[1]-m[0]+1
    nl=n[1]-n[0]+1
    ll=[ml,nl,ml,nl]
    
    stack=[]
    
    
    for p in range(4):
        a=start[p][0]-mu[p][0]
        b=start[p][1]-mu[p][1]
        for h in range(ll[p]-1):
            
            a+=mu[p][0]
            b+=mu[p][1]
            if mark[a][b]:
                continue
            
            elif gray[a][b]<thresh:
                mark[a][b]=True
                stack.append([a,b])
                while len(stack)>0:
                    val=stack.pop(0)
                    i=val[0]
                    j=val[1]
        
                    if gray[i][j]<thresh:
                        new_onebit[i][j]=0
                        #new_gray[i][j]=0
                        for k in range(4):
                            ii=i+dfir[k][1]
                            jj=j+dfir[k][0]
                            if ii<m[1] and jj<n[1] and ii>m[0]-1 and jj>n[0]-1:
                                if mark[ii][jj]==False:
                                    mark[ii][jj]=True
                                    stack.append([ii,jj])
    
    return new_onebit#,new_gray


def seperate_continent(onebit,Range,thresh):
    #the input Range is a 2*2 list, example:[[x_start,x_end],[y_start,y_end]]
    #bfs trace base board=============================
    mark=np.zeros([len(onebit),len(onebit[0])],bool)
    
    m=Range[1]
    n=Range[0]
    
    continent=[]
    stack=[]
    
    iout=m[0]
    while iout<=m[1]:
        jout=n[0]
        while jout<=n[1]:
            if not mark[iout][jout] and onebit[iout][jout]:
                count=1
                sep=np.zeros([len(onebit),len(onebit[0])],np.uint8)
                xRange=[n[1],n[0]]
                yRange=[m[1],m[0]]
                mark[jout][iout]=True
                stack.append([jout,iout])
                while len(stack)>0:
                    val=stack.pop(0)
                    i=val[0]
                    j=val[1]
        
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
                            if ii<m[1] and jj<n[1] and ii>m[0]-1 and jj>n[0]-1:
                                if mark[ii][jj]==False:
                                    mark[ii][jj]=True
                                    count+=1
                                    stack.append([ii,jj])
                if count>smallist_area:
                    continent.append([sep,[xRange,yRange],thresh])
            jout+=1
        iout+=1
    
    
    return continent#new_onebit


    
#-#-#-#-#-#-#-#-#main------------------------------------------

#all kinds of images we need======================
#base_graph,
path=""
file="./erythrocyte/health/1_1.bmp"
from glob import glob
filename = glob("D:/program/vscode_workspace/private/data/project_image(CS)/unhealth/*.bmp")
#filename = ["D:/program/vscode_workspace/private/data/project_image(CS)/health/1_1.bmp"]

index = 0
for file in filename:
    try:
        rgb=clear_white_edge(cv2.imread(file),(255,255,255))
        Ogray=clear_white_edge(cv2.imread(file,0),255)
        gray=copy(Ogray)
        #length, hight about values===================================
        m=len(gray)
        n=len(gray[0])
        real_length=50
        Pixellength = real_length/n
        Rrange=[10,20]
        Rrange=[230,250]

        thresh=10
        Range=[[0,n-1],[0,m-1]]

        #operating_graph
        todraw=copy(rgb)
        onebit=np.array([[255 for j in range(n)] for i in range(m)],np.uint8)
        #mark=np.zeros([m,n],bool)
        onebit=trace_base_board(onebit,gray,thresh)

        #showCV("o0",onebit)
        #showCV("o0",gray)

        continents=seperate_continent(onebit,Range,thresh)
        #for i in continents:
        #    showCV('p',i[0])
        #print(len(continents))
        continents_gray=[cut_graph(gray,continents[i][0]) for i in range(len(continents))]

        while len(continents)>0:
            old_continent=continents.pop(-1)
            old_gray=continents_gray.pop(-1)
            new_thresh=old_continent[2]+dthresh
            Range=old_continent[1]
            new_onebit=trace_base_board(old_continent[0],old_gray,new_thresh,Range)
            new_continents=seperate_continent(new_onebit,Range,new_thresh)
            #print(len(new_continents))
            #print(new_thresh)
            if len(new_continents)>1:
                while len(new_continents)>0:
                    new_continent=new_continents.pop(0)
                    continents.append(new_continent)
                    continents_gray.append(cut_graph(old_gray,new_continent[0]))
            #else:
                #showCV("o0",old_continent[0])
        print(file)
        index += 1
        #showCV("o",continent_gray[1])
    except:
        pass

print("index:", index)



'''onebit=cv2.inRange(gray,85,255)
showCV("o0",onebit)
c=cv2.HoughCircles(onebit,cv2.HOUGH_GRADIENT,1,30,param1=10,param2=10,minRadius=Rrange[0],maxRadius=Rrange[1])[0]
new=draw_circles(onebit,c,125,draw_in_copy=False)
showCV("r",new)
'''
#==========================================
#C=cut_graph(rgb,onebit)
#showCV("pp",onebit)
#showCV("pp",C)



'''
#####
one_blood_gray=np.zeros((m,n),np.uint8)
one_blood_onebit=np.zeros((m,n),np.uint8)

stack=[]
yn=False
for i in range(m):
    for j in range(n):
        if onebit[i][j]==255:
            yn=True
            break
    if j!=n-1:
        break
stack.append([i,j])
mark=np.zeros([m,n],bool)
mark[i][j]=True

blood=[]

while len(stack)>0:
    val=stack.pop(0)
    i=val[0]
    j=val[1]
    if onebit[i][j]==255:
        one_blood_onebit[i][j]=255
        one_blood_gray[i][j]=gray[i][j]
        gray[i][j]=0
        onebit[i][j]=0
        
        blood.append([i,j])
        for k in range(4):
            ii=i+dfir[k][1]
            jj=j+dfir[k][0]
            if ii<m and jj<n and ii>-1 and jj>-1:
                if mark[ii][jj]==False:
                    mark[ii][jj]=True
                    stack.append([ii,jj])

reset_graph(mark,m,n)


showCV("pp",one_blood_onebit)


onebit=onebit_trace_base(one_blood_onebit,one_blood_gray,thresh+10)
gray=copy(one_blood_gray)
showCV("p",onebit)


#####
one_blood_gray=np.zeros((m,n),np.uint8)
one_blood_onebit=np.zeros((m,n),np.uint8)

stack=[]
yn=False
for i in range(m):
    for j in range(n):
        if onebit[i][j]==255:
            yn=True
            break
    if j!=n-1:
        break
stack.append([i,j])
mark=np.zeros([m,n],bool)
mark[i][j]=True

blood=[]

while len(stack)>0:
    val=stack.pop(0)
    i=val[0]
    j=val[1]
    if onebit[i][j]==255:
        one_blood_onebit[i][j]=255
        one_blood_gray[i][j]=gray[i][j]
        gray[i][j]=0
        onebit[i][j]=0
        
        blood.append([i,j])
        for k in range(4):
            ii=i+dfir[k][1]
            jj=j+dfir[k][0]
            if ii<m and jj<n and ii>-1 and jj>-1:
                if mark[ii][jj]==False:
                    mark[ii][jj]=True
                    stack.append([ii,jj])

reset_graph(mark,m,n)
showCV("pp",one_blood_onebit)



'''
#*#*#*#*#*#*#*#*#
