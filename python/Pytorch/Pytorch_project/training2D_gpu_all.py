import time
import numpy as np
from glob import glob

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './data'
delta = "1"
classify_phase = [5,1,3,7]
particle_data = ["20190804","6"]
number_of_particle = int(particle_data[1])*int(particle_data[1])

EPOCH = 1          
LR = 0.001  
BATCH_SIZE = 3
internet = [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 4)]

def get_train_data(time, N):

    def comb(ph1,ph2):
        return np.concatenate((ph1,ph2))

    file = np.load((path+'/train/{},BA_matrix_train,N={},delta={}.npz').format(time,N,delta))

    test_input = comb(comb(file["BA"][ 800:1000],file["BA"][1800:2000]),
                      comb(file["BA"][2800:3000],file["BA"][3800:4000]))
    test_target = comb(comb(file["phase"][ 800:1000],file["phase"][1800:2000]),
                       comb(file["phase"][2800:3000],file["phase"][3800:4000]))
    train_input = comb(comb(file["BA"][   0: 800],file["BA"][1000:1800]),
                       comb(file["BA"][2000:2800],file["BA"][3000:3800]))
    train_target = comb(comb(file["phase"][   0: 800],file["phase"][1000:1800]),
                        comb(file["phase"][2000:2800],file["phase"][3000:3800]))
    return [torch.tensor(test_input   ,dtype=torch.float64),
            torch.tensor(test_target,dtype=torch.float64),
            torch.tensor(train_input   ,dtype=torch.float64),
            torch.tensor(train_target,dtype=torch.float64)]

total_data = get_train_data(particle_data[0],particle_data[1])
test_data  = TensorDataset(total_data[0],total_data[1])
train_data = TensorDataset(total_data[2],total_data[3])

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
cnn = cnn.cuda() 

def Accuracy(data):        
    s = 0
    for step, (b_x, b_y) in enumerate(data):            
        a = torch.reshape(b_x,(-1,1,number_of_particle,number_of_particle))   
        a = a.cuda()
        output = cnn(a.float())         
        if(int(b_y.numpy())==int(classify_phase[0]) and 
           output[0][0]>output[0][1] and output[0][0]>output[0][2] and output[0][0]>output[0][3]):
            s += 1 
        elif(int(b_y.numpy())==int(classify_phase[1]) and 
             output[0][1]>output[0][0] and output[0][1]>output[0][2] and output[0][1]>output[0][3]):                
            s += 1
        elif(int(b_y.numpy())==int(classify_phase[2]) and 
             output[0][2]>output[0][0] and output[0][2]>output[0][1] and output[0][2]>output[0][3]):                
            s += 1
        elif(int(b_y.numpy())==int(classify_phase[3]) and 
             output[0][3]>output[0][0] and output[0][3]>output[0][1] and output[0][3]>output[0][2]):                
            s += 1
    return s/len(data)

def main():
    acc = []  
    train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)  
    loss_func = nn.CrossEntropyLoss()   
    loss_func = loss_func.cuda() 
    for epoch in range(EPOCH):
        print("epoch:"+str(epoch)+"\n")
        
        for step, (b_x, b_y) in enumerate(train_dataloader):   
            a = torch.reshape(b_x,(-1,1,number_of_particle,number_of_particle))
            b = torch.tensor((b_y.numpy()>np.mean(classify_phase))*1.)
            b = []
            for i in b_y.numpy():
                if(int(i)==int(classify_phase[0])):
                    b.append(0)
                elif(int(i)==int(classify_phase[1])):
                    b.append(1)
                elif(int(i)==int(classify_phase[2])):
                    b.append(2)
                elif(int(i)==int(classify_phase[3])):
                    b.append(3)
            b = torch.tensor(b)
            a = a.cuda()
            b = b.cuda()
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
            file = np.load((path+'/test/{},BA_matrix_test,N={},delta={}.npz').format(particle_data[0],particle_data[1],delta))            
            test = TensorDataset(torch.tensor(file["BA"]),torch.tensor(file["phase"]))
            tmp = Accuracy(test)
            print("  total_predict :"+str(tmp))
            acc.append(tmp)
    print("\n")
    print(acc)
    torch.save(cnn, time.strftime("%Y%m%d%H%M", time.localtime())+",phase="+str(classify_phase)+",N="+particle_data[1]+',gpu.pkl')
    
if __name__ == '__main__':
    main()
