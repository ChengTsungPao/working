import cv2
import bfs_all as bfs
import numpy as np

flag = True
while(flag):
    choose = int(input("health or unhealth (0 or 1) : "))
    if(choose==1):
        target = "unhealth_bfs"
        # filename=["unhealth1.bmp", "unhealth2.bmp", "unhealth3.bmp", "unhealth4.bmp"]
        # length = [50, 51.9, 55.6, 58.8]
        # filename=["unhealth5.bmp", "unhealth6.bmp", "unhealth7.bmp", "unhealth8.bmp"]
        # length = [50, 50, 50, 50]
        filename=["unhealth9.bmp", "unhealth10.bmp", "unhealth11.bmp", "unhealth12.bmp"]
        length = [80, 80, 80, 80]
        flag = False
    elif(choose==0):
        target = "health_bfs"
        #filename=["health1.bmp", "health2.bmp"]
        filename=["health3.bmp", "health4.bmp"]
        filename=["health4.bmp"]
        length = [50, 50]
        flag = False
    else:
        print("please input the correct input!!!\n")



data = []
path = "./erythrocyte/"
Rrange=[10,40]
thresh=50

for i, file in enumerate(filename):
    try:
        data += bfs.radius(path, file, Rrange, thresh, length[i])
    except:
        pass


np.savez(path+target, r = np.array(data))
print(len(data))
f = np.load(path+target+".npz", allow_pickle=True)
print(f.files)
print(f[f.files[0]])


# print(len(data))
# np.savez(path+str(choose), r = np.array(data))
# f1 = np.load(path+str(0)+".npz", allow_pickle=True)
# f2 = np.load(path+str(1)+".npz", allow_pickle=True)
# import matplotlib.pylab as plt
# plt.scatter(f1["r"][:,0], f1["r"][:,1])
# plt.scatter(f2["r"][:,0], f2["r"][:,1])
# plt.show()
