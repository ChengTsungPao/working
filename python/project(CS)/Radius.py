import matplotlib.pylab as plt
import numpy as np
from PIL import Image
import copy

dx = -10
lineweight = 10
filename = "test1.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/"

im = Image.open(path+filename)
L = im.convert("L")

data = copy.copy(np.array(L))
bright = np.zeros(len(data[0]))
row = int(len(data)/2)+dx
for col in range(len(data[0])):
    bright[col] = data[row][col]
    for i in range(int(row-lineweight/2),int(row+lineweight/2)):
        data[i][col] = 0        

def IndexVal(arr,s):
    if(s=="min"):
        index = [len(arr)//3,len(arr)*2//3]
        val = np.min(arr[index[0]:index[1]])
    elif(s=="max-right"):
        index = [0,len(arr)//3]
        val = np.max(arr[index[0]:index[1]])
    elif(s=="max-left"):
        index = [len(arr)*2//3,len(arr)]
        val = np.max(arr[index[0]:index[1]])
    else:
        print("please input the correct mpde")
        return 0
    return np.where(arr[index[0]:index[1]]==val)[0][0]+index[0],val        

r = np.linspace(0,10,len(bright))
min_center = IndexVal(bright,"min")
max_right = IndexVal(bright,"max-right")
max_left = IndexVal(bright,"max-left")
print("\nMin pos and value:\n   ", end="")
print(r[min_center[0]],min_center[1])
print("\nMax-right pos and value:\n   ", end="")
print(r[max_right[0]],max_right[1])
print("\nMax-left pos and value:\n   ", end="")
print(r[max_left[0]],max_left[1])

plt.subplot(121)
plt.title("Bright Image")
plt.axis('off')
plt.imshow(data)
plt.subplot(122)
plt.title("Origin Image")
plt.axis('off')
plt.imshow(im)
plt.show()

plt.scatter([r[min_center[0]],r[max_right[0]],r[max_left[0]]],[min_center[1],max_right[1],max_left[1]],color = "r")
plt.title("Calculate Bright")
plt.xlabel("width (\u03BCm)")
plt.ylabel("brightness")
plt.plot(r,bright)
plt.show()

