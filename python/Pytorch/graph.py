import numpy as np
from glob import glob
import matplotlib.pylab as plt

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './data'
filename = '20190807154918,phase=[5, 1],gpu.pkl'

classify_phase = [5,1]
particle_data = ["20190804","6"]
number_of_particle = int(particle_data[1])*int(particle_data[1])

def get_test_data(data,phase):    
    cut = [len(data["phase"]),0]     
    for i in range(len(data["phase"])):        
        if(cut[0] > i and int(data["phase"][i])==phase):
            cut[0] = i
        if(cut[1] < i and int(data["phase"][i])==phase):
            cut[1] = i  
    return data["BA"][cut[0]:cut[1]+1],data["phase"][cut[0]:cut[1]+1]

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

model = torch.load(filename)

def Probability(data,target):
    p = []
    for i in range(len(data)):
        output = model(torch.tensor(data[i]).reshape(1,1,number_of_particle,number_of_particle).float().cuda())
        p.append(output[0][target])
    return p

file = np.load((path+'/test/{},BA_matrix_test,N={},delta=1.npz').format(particle_data[0],particle_data[1]))
target1 = Probability(get_test_data(file,classify_phase[0])[0],0) 
target2 = Probability(get_test_data(file,classify_phase[1])[0],0) 
plt.plot(range(len(target1)+len(target2)),target1+target2)

#target3 = Probability(get_test_data(file,classify_phase[0])[0],1) 
#target4 = Probability(get_test_data(file,classify_phase[1])[0],1) 
#plt.plot(range(len(target3)+len(target4)),target3+target4)

plt.show()


