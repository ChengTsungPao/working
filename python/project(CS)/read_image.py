import matplotlib.pylab as plt
import numpy as np
from PIL import Image

dx = -10
lineweight = 10
filename = "test1.bmp"
path = "D:/program/vscode_workspace/private/data/project_image(CS)/"

im = Image.open(path+filename)
L = im.convert("L")
data_self = []  
data_lib = [] 
for y in range(im.size[1]):
    data_self.append([])
    data_lib.append([])
    for x in range(im.size[0]):
        data_self[y].append(im.getpixel((x,y)))
        data_lib[y].append(L.getpixel((x,y)))

bright_self = np.zeros(len(data_self[0]))
bright_lib = np.zeros(len(data_lib[0]))
row = int(len(data_self)/2)+dx
for col in range(len(data_self[0])):
    bright_self[col] = 0.2126*data_self[row][col][0] + 0.7152*data_self[row][col][0] + 0.0722*data_self[row][col][0]
    bright_lib[col] = data_lib[row][col]
    for i in range(int(row-lineweight/2),int(row+lineweight/2)):
        data_self[i][col] = (0,0,0)
        data_lib[i][col] = 0        

plt.subplot(234)
plt.title("Calculate by myself")
plt.xlabel("width(\u03BCm)")
plt.ylabel("brightness")
plt.plot(np.linspace(0,10,len(bright_self)),bright_self)
plt.subplot(235)
plt.title("Calculate by library")
plt.xlabel("width (\u03BCm)")
plt.ylabel("brightness")
plt.plot(np.linspace(0,10,len(bright_lib)),bright_lib)

plt.subplot(231)
plt.title("Calculate by myself")
plt.axis('off')
plt.imshow(data_self)
plt.subplot(232)
plt.title("Calculate by library")
plt.axis('off')
plt.imshow(data_lib)
plt.subplot(233)
plt.title("Origin Image")
plt.axis('off')
plt.imshow(im)
plt.show()

