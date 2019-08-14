import numpy as np
from glob import glob
import matplotlib.pylab as plt

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset

path = 'D:/program/vscode_workspace/private/data/project_data'
#path = './data'
filename = input("input the filename: ")
#graph = input("input the graph name: ") 
#npzname = input("input the npzname: ")

classify = filename.split("[")[1].split("]")[0]
classify = classify.split(",")
classify_phase = []
for i in range(len(classify)):
    classify_phase.append(int(classify[i]))


particle_data = ["20190804","6"]
particle_data[1] = filename.split("N=")[1][0]
number_of_particle = int(particle_data[1])*int(particle_data[1])

if(abs(classify_phase[0]-classify_phase[1])==1):
    if(classify_phase[0]==1):
        line = "mu=1.0"
    elif(classify_phase[0]==3):
        line = "mu=3.0"
    elif(classify_phase[0]==7):
        line = "mu=5.0"
    elif(classify_phase[0]==5):
        line = "mu=-1.0"
elif(classify_phase[0]%2==1):
    line = "delta=1"
elif(classify_phase[0]%2==0):
    line = "delta=-1"
else:
    print("please input the correct phase !!!")

def get_test_data(phase):  
    BA = []
    file = np.load((path+'/test/{},BA_matrix_test,N={},{}.npz').format(particle_data[0],particle_data[1],line))
    for i in range(len(phase)):
        cut = [len(file["phase"]),0]     
        for j in range(len(file["phase"])):        
            if(cut[0] > j and int(file["phase"][j])==phase[i]):
                cut[0] = j
            if(cut[1] < j and int(file["phase"][j])==phase[i]):
                cut[1] = j 
        BA += file["BA"][cut[0]:cut[1]+1].tolist()        

    return np.array(BA)

class CNN(nn.Module):
    def __init__(self,conv1,conv2,linear):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(  
            nn.Conv2d(
                in_channels=conv1[0],      
                out_channels=conv1[1],    
                kernel_size=conv1[2],     
                stride=conv1[3],          
                padding=conv1[4],      
            ),      
            nn.ReLU(),    
            nn.MaxPool2d(kernel_size=2), 
        )
        self.conv2 = nn.Sequential(  
            nn.Conv2d(conv2[0], conv2[1], conv2[2], conv2[3], conv2[4]),  
            nn.ReLU(),  
            nn.MaxPool2d(2),  
        )
        self.layer = nn.Linear(linear[0], linear[1])  
        self.out = nn.Linear(linear[1], linear[2])  
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   
        x = self.layer(x)
        x = self.out(x)
        output = nn.functional.softmax(x,dim=1)
        return output

model = torch.load("D:/program/vscode_workspace/private/data/project_train/model/"+filename)

def Probability(data,target):
    p = []
    for i in range(len(data)):
        output = model(torch.tensor(data[i]).reshape(1,1,number_of_particle,number_of_particle).float().cuda())
        #output = model(torch.tensor(data[i]).reshape(-1,int(particle_data[1]),int(particle_data[1]),int(particle_data[1]),int(particle_data[1])).float().cuda())
        p.append(output[0][target].cpu().data.numpy())
    return p

target = []
for i in range(len(classify_phase)):
    target.append(Probability(get_test_data(classify_phase),i)) 
    plt.plot(range(len(target[i])),target[i],"o")

plt.show()

#plt.savefig(graph)

'''
if(len(classify_phase)==2):
    np.savez("./npzfile/"+npzname,phase1 = target[0],phase2 = target[1])
elif(len(classify_phase)==4):
    np.savez("./npzfile/"+npzname,phase1 = target[0],phase2 = target[1],phase3 = target[2],phase4 = target[3])
else:
    print("please input the correct phase !!!")    
'''



