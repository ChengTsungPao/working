import cv2
import numpy as np
import matplotlib.pyplot as plt


def showCV(title,image):
    cv2.imshow(title,image)
    cv2.waitKey()
    cv2.destroyAllWindows()

dirac=[[1,0],[0,1],[1,1],[1,-1]]
dfir=[[1,0],[-1,0],[0,1],[0,-1]]

thresh=10


#all kinds of images we need======================
path = "./erythrocyte/"
file="good1.bmp"
rgb=cv2.imread(path+file)
todraw=cv2.imread(path+file)
todraw2=cv2.imread(path+file)
gray=cv2.imread(path+file,0)



dfs_onebit=[]
mark=[]
m=len(gray)
n=len(gray[0])

for i in range(m):
    mark.append([])
    dfs_onebit.append([])
    for j in range(n):
        mark[i].append(False)
        dfs_onebit[i].append(0)
dfs_onebit=np.array(dfs_onebit,np.uint8)
stack=[]

for i in range(m):
    for j in range(n):
        if gray[i][j]<thresh:
            break
    if j<n:
        break

print(i,j)
stack.append([i,j])
print(stack)
stack.append(0)
stack=stack[0:len(stack)-1]
print(stack)

#print(mark)
while len(stack)>0:
    l=len(stack)
    #print(l)
    i=stack[l-1][0]
    j=stack[l-1][1]
    stack=stack[0:l-1]
    #print(i,j)
    if mark[i][j]==False and gray[i][j]<thresh:
        mark[i][j]=True
        #print("in")
        dfs_onebit[i][j]=255
        for k in range(4):
            ii=i+dfir[k][1]
            jj=j+dfir[k][0]
            if ii<m and jj<n and ii>-1 and jj>-1 and mark[ii][jj]==False:
                stack.append([ii,jj])


showCV('ppp',dfs_onebit)

'''
s=0
for i in range(len(gray)):
    for j in range(len(gray[0])):
        s+=gray[i][j]
s/=len(gray)*len(gray[0])
s*=1.5


onebit=cv2.inRange(gray,s,s+30)

'''

