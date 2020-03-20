import cv2
import numpy as np
import matplotlib.pyplot as plt
from find import find, trace, take_line


def showCV(title,image):
    return
    # cv2.imshow(title,image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

def reset_graph(boolean_graph,m,n):
    for i in range(m):
        for j in range(n):
            boolean_graph[i][j]=False
    return boolean_graph

def radius(path, file, Rrange, thresh, length):
    rgb=cv2.imread(path+file)
    todraw=cv2.imread(path+file)
    todraw2=cv2.imread(path+file)
    Ogray=cv2.imread(path+file,0)
    gray=cv2.imread(path+file,0)
    Pixellength = length/len(gray[0])
    #=================================================
    m=len(gray)
    n=len(gray[0])
    stack=[]
    mark=[]
    onebit=[]

    for i in range(m):
        mark.append([])
        onebit.append([])
        for j in range(n):
            mark[i].append(False)
            onebit[i].append(255)
    onebit=np.array(onebit,np.uint8)

    mu=[[1,0],[0,1],[-1,0],[0,-1]]
    ll=[m,n,m,n]
    start=[[0,0],[0,0],[m-1,n-1],[m-1,n-1]]
    dfir=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
    dirac=[[1,0],[0,1],[1,1],[1,-1]]

    #showCV("pp",onebit)
    #bfs=============================
    #together
    '''
    for p in range(4):
        a=start[p][0]
        b=start[p][1]
        for h in range(ll[p]-1):
            
            a+=mu[p][0]
            b+=mu[p][1]
            if mark[a][b]:
                pass
            
            elif gray[a][b]<=thresh:
                mark[a][b]=True
                stack.append([a,b])
                while len(stack)>0:
                    val=stack.pop(0)
                    i=val[0]
                    j=val[1]
        
                    if gray[i][j]<thresh:
                        onebit[i][j]=0
                        gray[i][j]=0
                        for k in range(4):
                            ii=i+dfir[k][1]
                            jj=j+dfir[k][0]
                            if ii<m and jj<n and ii>-1 and jj>-1:
                                if mark[ii][jj]==False:
                                    mark[ii][jj]=True
                                    stack.append([ii,jj])
                    else:
                        mark[i][j]=False
                #showCV("pp",onebit)
            
            else:
                mark[a][b]=True
                stack.append([a,b])
                while len(stack)>0:
                    val=stack.pop(0)
                    i=val[0]
                    j=val[1]
        
                    if gray[i][j]>=thresh:
                        onebit[i][j]=0
                        gray[i][j]=0
                        for k in range(4):
                            ii=i+dfir[k][1]
                            jj=j+dfir[k][0]
                            if ii<m and jj<n and ii>-1 and jj>-1:
                                if mark[ii][jj]==False:
                                    mark[ii][jj]=True
                                    stack.append([ii,jj])
                    else:
                        mark[i][j]=False
                #showCV("pp",onebit)
    '''

    for p in range(4):
        a=start[p][0]
        b=start[p][1]
        for h in range(ll[p]-1):
            
            a+=mu[p][0]
            b+=mu[p][1]
            if mark[a][b]:
                pass
            
            elif gray[a][b]<thresh:
                mark[a][b]=True
                stack.append([a,b])
                while len(stack)>0:
                    val=stack.pop(0)
                    i=val[0]
                    j=val[1]
        
                    if gray[i][j]<thresh:
                        onebit[i][j]=0
                        gray[i][j]=0
                        for k in range(4):
                            ii=i+dfir[k][1]
                            jj=j+dfir[k][0]
                            if ii<m and jj<n and ii>-1 and jj>-1:
                                if mark[ii][jj]==False:
                                    mark[ii][jj]=True
                                    stack.append([ii,jj])
                    else:
                        mark[i][j]=False
    reset_graph(mark,m,n)
    showCV("pp",onebit)
    #showCV("pp",gray)

    for p in range(4):
        a=start[p][0]
        b=start[p][1]
        for h in range(ll[p]-1):
            
            a+=mu[p][0]
            b+=mu[p][1]
            if mark[a][b]:
                pass
            elif onebit[a][b]==255:
                mark[a][b]=True
                stack.append([a,b])
                while len(stack)>0:
                    val=stack.pop(0)
                    i=val[0]
                    j=val[1]
        
                    if onebit[i][j]==255:
                        onebit[i][j]=0
                        gray[i][j]=0
                        for k in range(4):
                            ii=i+dfir[k][1]
                            jj=j+dfir[k][0]
                            if ii<m and jj<n and ii>-1 and jj>-1:
                                if mark[ii][jj]==False:
                                    mark[ii][jj]=True
                                    stack.append([ii,jj])
                    else:
                        mark[i][j]=False

    showCV("p",onebit)        

    for i in range(m):
        for j in range(n):
            if gray[i][j]<thresh:
                break
        if i!=n-1:
            break

    stack.append([i,j])
    mark[i][j]=True

    while len(stack)>0:
        val=stack.pop(0)
        i=val[0]
        j=val[1]
        if gray[i][j]<thresh:
            onebit[i][j]=0
            for k in range(4):
                ii=i+dfir[k][1]
                jj=j+dfir[k][0]
                if ii<m and jj<n and ii>-1 and jj>-1:
                    if mark[ii][jj]==False:
                        mark[ii][jj]=True
                        stack.append([ii,jj])

    mark = reset_graph(mark,m,n)

    #onebit=cv2.inRange(gray, 10, 255)
    #onebit=np.load("dfs_onebit.npy")

    #出edges圖==================================

    showCV('yyo',onebit)
    for p in range(4):
        a=start[p][0]
        b=start[p][1]
        for h in range(ll[p]-1):
            a+=mu[p][0]
            b+=mu[p][1]
            if onebit[a][b]==255:
                mark[a][b]=True
                stack.append([a,b])
        
            while len(stack)>0:
                val=stack.pop(0)
                i=val[0]
                j=val[1]

                if onebit[i][j]==255:
                    onebit[i][j]=0
                    gray[i][j]=0
                    for k in range(4):
                        ii=i+dfir[k][1]
                        jj=j+dfir[k][0]
                        if ii<m and jj<n and ii>-1 and jj>-1:
                            if mark[ii][jj]==False:
                                mark[ii][jj]=True
                                stack.append([ii,jj])

    reset_graph(mark,m,n)
    #showCV("pp",onebit)
    #showCV("pp",gray)

    #=============================================
    #==============================================

    #cv2.circle(edges,(xx[1],xx[0]),2,255,3)
    #showCV("pp",edges)

    #cv2.circle(onebit,(xx[1],xx[0]),2,125,3)
    R = []
    inRadius=[]
    outRadius=[]
    yn=True

    while yn==True:
        one_blood_gray=np.zeros((m,n),np.uint8)
        one_blood_onebit=np.zeros((m,n),np.uint8)
        
        blood=[]
        yn=False
        for i in range(m):
            for j in range(n):
                if onebit[i][j]==255:
                    yn=True
                    break
            if j!=n-1:
                break
        stack.append([i,j])
        mark[i][j]=True
        
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
        
        #showCV("pp",one_blood_gray)
        
        #算整顆平均值，轉onebit邊圖==============================
        #edges=np.load("edges.npy")
        #showCV("pp",edges)
        try:
            s=0
            for i in blood:
                s+=one_blood_gray[i[0]][i[1]]
            #print(blood)
            s/=len(blood)
            #print(s)
            one_blood_onebit=cv2.inRange(one_blood_gray,s-15,s+15)
            
            #===========================================
            
            #定位圓心======================================
            center=[]
            circles = cv2.HoughCircles(one_blood_onebit,cv2.HOUGH_GRADIENT,1,1000,param1=10,param2=1,minRadius=Rrange[0],maxRadius=Rrange[1])
            circles = np.uint16(np.around(circles))
            
            
            for i in circles[0,:]:  
                #rad = (i[0],i[1],i[2],(0,255,0),2)
                center.append([i[0],i[1]])
            
                #cv2.circle(onebit,(i[0],i[1]),i[2],125,2) # draw the outer circle
                #cv2.circle(onebit,(i[0],i[1]),2,125,3) # draw the center of the circle
            
            
            xx=circles[0][0]
            
            xx=xx[0:2]
            #print(xx)
            
            
            #cv2.circle(onebit,(xx[0],xx[1]),2,255,3)
            #showCV("pp",onebit)
            
            xx=find(one_blood_onebit,xx)
            lines,centerI=take_line(one_blood_gray,xx)
            l,c,r=trace(lines[0],centerI[0])
                
            #print(l,c,r)
            
            val=(float(one_blood_gray[xx[1]][c])+float(one_blood_gray[xx[1]][r])+float(one_blood_gray[xx[1]][c])+float(one_blood_gray[xx[1]][l]))/4
            #print(val)
            #=================================================
            
            one_blood_onebit=cv2.inRange(one_blood_gray,val,255)
            #showCV("pp",one_blood_onebit)
            
            edge=cv2.Canny(one_blood_onebit, 1,1 )
            
            i=xx[1]
            while edge[i][xx[0]]==0:
                i+=1
            
            stack.append([i,xx[0]])
            mark[i][xx[0]]==True
            ed=[]
            
            #cv2.circle(edges,(xx[0],i),2,255,3)
            #showCV("pp",edge)
            
            while len(stack)>0:
                val=stack.pop(0)
                i=val[0]
                j=val[1]
                if edge[i][j]==255:     
                    ed.append([i,j])
                    
                    for k in range(8):
                        ii=i+dfir[k][1]
                        jj=j+dfir[k][0]
                        if ii<m and jj<n and ii>-1 and jj>-1:
                            if mark[ii][jj]==False:
                                mark[ii][jj]=True
                                stack.append([ii,jj])
            reset_graph(mark,m,n)
            
            #print(ed)
            dim = 10
            
            in_r=[]
            
            for k in range(dim):
                tmp = 0
                for t in range(len(ed)//dim):
                    i=int(ed[k*(len(ed)//dim)+t][0])-int(xx[1])
                    j=int(ed[k*(len(ed)//dim)+t][1])-int(xx[0])
                    tmp+=(i**2+j**2)**0.5
                in_r.append(tmp*Pixellength/(len(ed)//dim))
            
            #in_r/=len(ed)
            #in_r*=Pixellength
            inRadius.append(in_r)
            print(in_r)
            
            #out_radius===================
            val=(float(one_blood_gray[xx[1]][r])+float(one_blood_gray[xx[1]][c])+thresh*2)/4
            
            one_blood_onebit=cv2.inRange(one_blood_gray,val,255)
            edge=cv2.Canny(one_blood_onebit, 1,1 )
            
            i=0
            while edge[i][xx[0]]==0:
                i+=1
            
            #showCV("pp",edge)
            
            stack.append([i,xx[0]])
            mark[i][xx[0]]==True
            ed=[]
            
            
            while len(stack)>0:
                val=stack.pop(0)
                i=val[0]
                j=val[1]
                if edge[i][j]==255:     
                    ed.append([i,j])
                    
                    for k in range(8):
                        ii=i+dfir[k][1]
                        jj=j+dfir[k][0]
                        if ii<m and jj<n and ii>-1 and jj>-1:
                            if mark[ii][jj]==False:
                                mark[ii][jj]=True
                                stack.append([ii,jj])
            reset_graph(mark,m,n)
            
            out_r=[]
            
            for k in range(dim):
                tmp = 0
                for t in range(len(ed)//dim):                    
                    i=int(ed[k*(len(ed)//dim)+t][0])-int(xx[1])
                    j=int(ed[k*(len(ed)//dim)+t][1])-int(xx[0])
                    tmp+=(i**2+j**2)**0.5
                out_r.append(tmp*Pixellength/(len(ed)//dim))
            
            #out_r/=len(ed)
            #out_r*=Pixellength
            
            outRadius.append(out_r)
            
            print(out_r)
            R.append(in_r + out_r)
            #print(len(in_r + out_r))
            showCV("p",onebit)
            #showCV("pp",one_blood_onebit)
            
        except:
            pass
    #===================

    print(inRadius)
    print(outRadius)
    return R

if __name__=="__main__":

    Rrange=[10,40]
    thresh=50
    length = 50
    length = 80


    #all kinds of images we need======================
    path="./erythrocyte/"
    file="bad1.bmp"
    file="health1.bmp"
    file="unhealth11.bmp"
    r = radius(path, file, Rrange, thresh, length)
    print("index : ",len(r)//2)