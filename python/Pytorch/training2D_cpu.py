import time
import numpy as np
from glob import glob

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './data'
classify_phase = [5,1]
particle_data = ["20190804","6"]
number_of_particle = int(particle_data[1])*int(particle_data[1])

EPOCH = 1          
LR = 0.001  
BATCH_SIZE = 3
internet = [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 2)]

def get_train_data(time, N, phase=[5,1]):

    def move(ph):
        if(ph==5):
            m = 0
        elif(ph==1):
            m = 1000
        elif(ph==3):
            m = 2000
        elif(ph==7):
            m = 3000
        else:
            print("error")
        return m

    file = np.load((path+'/train/{},BA_matrix_train,N={},delta=1.npz').format(time,N))

    test_input = np.concatenate((file["BA"][800 + move(phase[0]) : 1000 + move(phase[0])],
                                 file["BA"][800 + move(phase[1]): 1000 + move(phase[1])]))
    test_target = np.concatenate((file["phase"][800 + move(phase[0]) : 1000 + move(phase[0])],
                                  file["phase"][800 + move(phase[1]) : 1000 + move(phase[1])]))
    train_input = np.concatenate((file["BA"][0 + move(phase[0]) : 800 + move(phase[0])],
                                  file["BA"][0 + move(phase[1]) : 800 + move(phase[1])]))
    train_target = np.concatenate((file["phase"][0 + move(phase[0]) : 800 + move(phase[0])],
                                   file["phase"][0 + move(phase[1]) : 800 + move(phase[1])]))
    return [torch.tensor(test_input   ,dtype=torch.float64),
            torch.tensor(test_target,dtype=torch.float64),
            torch.tensor(train_input   ,dtype=torch.float64),
            torch.tensor(train_target,dtype=torch.float64)]

total_data = get_train_data(particle_data[0],particle_data[1],classify_phase)
test_data  = TensorDataset(total_data[0],total_data[1])
train_data = TensorDataset(total_data[2],total_data[3])

def get_test_data(data,phase):    
    cut = [len(data["phase"]),0]     
    for i in range(len(data["phase"])):        
        if(cut[0] > i and int(data["phase"][i])==phase):
            cut[0] = i
        if(cut[1] < i and int(data["phase"][i])==phase):
            cut[1] = i  
    return data["BA"][cut[0]:cut[1]],data["phase"][cut[0]:cut[1]]

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

cnn = CNN(internet[0],internet[1],internet[2])   

def Accuracy(data):        
    s = 0
    for step, (b_x, b_y) in enumerate(data):            
        a = torch.reshape(b_x,(-1,1,number_of_particle,number_of_particle))   
        output = cnn(a.float())         
        if(b_y.numpy()<np.mean(classify_phase) and output[0][0]>output[0][1]):
            s += 1 
        elif(b_y.numpy()>np.mean(classify_phase) and output[0][0]<output[0][1]):                
            s += 1
    return s/len(data) 

def main():    
    acc = []  
    train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)  
    loss_func = nn.CrossEntropyLoss()    
    for epoch in range(EPOCH):
        print("epoch:"+str(epoch)+"\n")
        
        for step, (b_x, b_y) in enumerate(train_dataloader):   
            a = torch.reshape(b_x,(-1,1,number_of_particle,number_of_particle))
            b = torch.tensor((b_y.numpy()>np.mean(classify_phase))*1.)
            output = cnn(a.float())   
            optimizer.zero_grad()        
            loss = loss_func(output, b.long())             
            loss.backward()               
            optimizer.step()             
            if(step%200==0):          
                print("number of data:"+str(step))
                print("output:\n"+str(output.data))
                print("target:\n"+str(b.data))
                print("\n")

        if(epoch%10==0):        
            print("epoch:"+str(epoch))
            print("  training:"+str(Accuracy(train_data)))
            print("  predict :"+str(Accuracy(test_data)))
            file = np.load((path+'/test/{},BA_matrix_test,N={},delta=1.npz').format(particle_data[0],particle_data[1]))            
            test1 = TensorDataset(torch.tensor(get_test_data(file,classify_phase[0])[0]),torch.tensor(get_test_data(file,classify_phase[0])[1]))
            test2 = TensorDataset(torch.tensor(get_test_data(file,classify_phase[1])[0]),torch.tensor(get_test_data(file,classify_phase[1])[1]))
            tmp = (Accuracy(test1)*len(test1)+Accuracy(test2)*len(test2))/(len(test1)+len(test2))
            print("  total_predict :"+str(tmp))
            acc.append(tmp)
    print("\n")
    print(acc)
    torch.save(cnn, time.strftime("%Y%m%d%H%M%S", time.localtime())+",phase="+str(classify_phase)+',cpu.pkl')


if __name__ == '__main__':
    main()






